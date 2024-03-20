import scrapy
from scrapy.http import Request, FormRequest
from scrapy_splash import SplashRequest
import json
import re
import random
from scrapy.crawler import CrawlerProcess

class LinkedInProfileScraper(scrapy.Spider):
    name = "lpp"
    items = []
    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.jsonl': {'format': 'jsonlines'}},
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_DEBUG': True,
        'DOWNLOAD_TIMEOUT': 301,
        'DOWNLOAD_DELAY': 10,
        'DOWNLOAD_DELAY_RANDOMIZE': True,
        'DOWNLOAD_DELAY_RANDOM_RANGE': (3, 20),
    }

    def __init__(self, *args, **kwargs):
        super(LinkedInProfileScraper, self).__init__(*args, **kwargs)
        self.user_agents = [
          
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            
          
            'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
            
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
           
        ]
        

    def start_requests(self):
        self.user_agents_cycle = iter(self.user_agents)
        profile_list = ['shreyas-deodhare']
        for profile in profile_list:
            headers = {'User-Agent': self.user_agents_cycle}
            linkedin_people_url = f'https://www.linkedin.com/in/{profile}/'
            yield SplashRequest(url=linkedin_people_url, callback=self.parse_profile, meta={'profile': profile, 'linkedin_url': linkedin_people_url,'headers':headers})

    def parse_profile(self, response):
        item = {}
        item['profile'] = response.meta['profile']
        item['url'] = response.meta['linkedin_url']
        self.items.append(item)

        """
        SUMMARY SECTION
        """
        summary_box = response.css("section.top-card-layout")
        item['name'] = summary_box.css("h1::text").get().strip()
        item['description'] = summary_box.css("h2::text").get().strip()

        try:
            item['location'] = summary_box.css('div.top-card__subline-item::text').get()
        except:
            item['location'] = summary_box.css('span.top-card__subline-item::text').get().strip()
            if 'followers' in item['location'] or 'connections' in item['location']:
                item['location'] = ''

        item['followers'] = self.extract_numeric(summary_box.css('span.top-card__subline-item > span::text').get())
        item['connections'] = self.extract_numeric(summary_box.css('span.top-card__subline-item > span::text').get())

        """
        ABOUT SECTION
        """
        item['about'] = response.css('section.summary div.core-section-container__content p::text').get(default='')

        """
        EXPERIENCE SECTION
        """
        item['experience'] = []
        experience_blocks = response.css('li.experience-item')
        for block in experience_blocks:
            experience = {}
            experience['organisation_profile'] = block.css('h4 a::attr(href)').get(default='').split('?')[0]
            experience['location'] = block.css('p.experience-item__location::text').get(default='').strip()

            try:
                experience['description'] = block.css('p.show-more-less-text__text--more::text').get().strip()
            except Exception as e:
                experience['description'] = block.css('p.show-more-less-text__text--less::text').get(default='').strip()

            try:
                date_ranges = block.css('span.date-range time::text').getall()
                if len(date_ranges) == 2:
                    experience['start_time'] = date_ranges[0]
                    experience['end_time'] = date_ranges[1]
                    experience['duration'] = block.css('span.date-range__duration::text').get()
                elif len(date_ranges) == 1:
                    experience['start_time'] = date_ranges[0]
                    experience['end_time'] = 'present'
                    experience['duration'] = block.css('span.date-range__duration::text').get()
            except Exception as e:
                experience['start_time'] = ''
                experience['end_time'] = ''
                experience['duration'] = ''

            item['experience'].append(experience)

        """
        EDUCATION SECTION
        """
        item['education'] = []
        education_blocks = response.css('li.education__list-item')
        for block in education_blocks:
            education = {}
            education['organisation'] = block.css('h3::text').get(default='').strip()
            education['organisation_profile'] = block.css('a::attr(href)').get(default='').split('?')[0]

            try:
                education['course_details'] = ''
                for text in block.css('h4 span::text').getall():
                    education['course_details'] = education['course_details'] + text.strip() + ' '
                education['course_details'] = education['course_details'].strip()
            except Exception as e:
                education['course_details'] = ''

            education['description'] = block.css('div.education__item--details p::text').get(default='').strip()

            try:
                date_ranges = block.css('span.date-range time::text').getall()
                if len(date_ranges) == 2:
                    education['start_time'] = date_ranges[0]
                    education['end_time'] = date_ranges[1]
                elif len(date_ranges) == 1:
                    education['start_time'] = date_ranges[0]
                    education['end_time'] = 'present'
            except Exception as e:
                education['start_time'] = ''
                education['end_time'] = ''

            item['education'].append(education)

        # Save item to text file
        self.save_to_text(item)
        yield item

    def save_to_text(self, item):
        with open(f'data/{self.name}_output.txt', 'a', encoding='utf-8') as file:
            file.write(json.dumps(item, indent=4, ensure_ascii=False))
            file.write('\n')

    def extract_numeric(self, text):
        if text:
            numeric_value = re.search(r'\d+', text)
            if numeric_value:
                return int(numeric_value.group())
        return 0


