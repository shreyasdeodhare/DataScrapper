import scrapy
from scrapy_splash import SplashRequest
import csv
from itertools import cycle

class DynamicSpider(scrapy.Spider):
    name = 'dynamic_spider'
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_DEBUG': True,
        'DOWNLOAD_TIMEOUT': 300,  
        'DOWNLOAD_DELAY' :  5, 
        'DOWNLOAD_DELAY_RANDOMIZE' :  True, 
        'DOWNLOAD_DELAY_RANDOM_RANGE'  :  (3, 7),

    }

    def __init__(self, *args, **kwargs):
        super(DynamicSpider, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_urls').split(',') if kwargs.get('start_urls') else []
        self.selectors = kwargs.get('selectors').split(',') if kwargs.get('selectors') else []
        self.results = []
        self.user_agents = cycle([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",

        ])

    def start_requests(self):
        urls = [
            # 'https://www.linkedin.com/in/yash-bhavsar-a62630208',
            'https://www.nseindia.com/', 

        ]
        for url in urls:
            user_agent = next(self.user_agents)
            headers = {
                "User-Agent": user_agent
            }
            yield SplashRequest(url, self.parse_result, args={'wait':20}, headers=headers)

    def parse_result(self, response):
        xpath_query="abc"
        item = {}
        for selector in self.selectors:
            elements = response.css(selector)
            if elements:
                self.logger.info(f"Data from elements matching selector '{selector}':")
                item[selector] = [element.xpath('string()').get().strip() for element in elements]
            elif selector=="href":
                item['text']=response.xpath('//a//text()').getall()
                item['links'] = response.xpath('//a/@href').getall()      
                
            # elif selector=="profile":
            #     description=response.xpath('//*[@id="profile-content"]/div/div[2]/div/div/main/section[5]/div[3]/div/div/div/span[2]/text()').get()
            #     if description:
            #       self.logger.info(f"Description extracted: '{description}'")
            #       item['description'] = description.strip()
            else:
                self.logger.warning("Description element not found.")
              
              
                
                for selector in self.selectors:

                      if selector.startswith('#'):  
                           table_id = selector[1:]  
                           xpath_query = f'//*[@id="[{table_id}]"]'
                      elif selector.startswith('.'):  
                          class_name = selector[1:]  
                          xpath_query = f'//table[contains(concat(" ", normalize-space(@class), " "), " {class_name} ")]'
                      else:
                          xpath_query=f'//table'
                          

            tables = response.xpath(xpath_query)
            for table in tables:
               item = {}
               rows = table.xpath('.//tr')
               for row in rows[1:]:
                  cells = row.xpath('.//td//text()').extract()
                  if cells:
                      item['table'] = selector
                      item['values'] = [cell.strip() for cell in cells if cell.strip()]
                      self.results.append(item)

        self.results.append(item)

        # item['links'] = response.xpath('//a/@href').getall()
        # item['paragraphs'] = response.xpath('//p//text()').getall()
        # item['headings'] = response.xpath('//h1//text() | //h2//text() | //h3//text() | //h4//text() | //h5//text() | //h6//text()').getall()
        # item['images'] = response.xpath('//img/@src').getall()
        # item['forms'] = response.xpath('//form').getall()
        # item['buttons'] = response.xpath('//button//text()').getall()
        # item['input_fields'] = response.xpath('//input').getall()
        # item['labels'] = response.xpath('//label//text()').getall()
        # item['list_items'] = response.xpath('//li//text()').getall()

        # item['tables'] = response.xpath('//table').getall()
        # item['span_texts'] = response.xpath('//span//text()').getall()
        # item['div_texts'] = response.xpath('//div//text()').getall()
        # item['strong_texts'] = response.xpath('//strong//text()').getall()
        # item['emphasized_texts'] = response.xpath('//em//text()').getall()
        # item['blockquote_texts'] = response.xpath('//blockquote//text()').getall()
        # item['pre_texts'] = response.xpath('//pre//text()').getall()

        # self.results.append(item)

    def closed(self, reason):
        self.save_to_csv(self.results)

    def save_to_csv(self, results):
        try:
            if results:
                with open('tables.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)

                    writer.writerow(["Selector", "Value"])
                    for result in results:
                        for key, value in result.items():
                            if isinstance(value, list) and all(isinstance(item, list) for item in value):

                                flattened_values = [sub_item for sublist in value for sub_item in sublist]

                                unique_values = list(set(flattened_values))
                                for val in unique_values:
                                    writer.writerow([key, val])
                            else:
                                writer.writerow([key, value])
                self.logger.info("Scraped data saved to 'table.csv'.")
            else:
                self.logger.warning("No data to save to CSV.")
        except Exception as e:
            self.logger.error(f"Error saving scraped data to Csv")


# import scrapy
# from scrapy_splash import SplashRequest
# import csv
# from itertools import cycle

# class DynamicSpider(scrapy.Spider):
#     name = 'dynamic_spider'
#     custom_settings = {
#         'AUTOTHROTTLE_ENABLED': True,
#         'AUTOTHROTTLE_DEBUG': True,
#         'DOWNLOAD_TIMEOUT': 300,  
#         'DOWNLOAD_DELAY' :  5, 
#         'DOWNLOAD_DELAY_RANDOMIZE' :  True, 
#         'DOWNLOAD_DELAY_RANDOM_RANGE'  :  (3, 7),

#     }

#     def __init__(self, *args, **kwargs):
#         super(DynamicSpider, self).__init__(*args, **kwargs)
#         self.start_urls = kwargs.get('start_urls').split(',') if kwargs.get('start_urls') else []
#         self.selectors = kwargs.get('selectors').split(',') if kwargs.get('selectors') else []
#         self.results = []
#         self.user_agents = cycle([
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",

#         ])

#     def start_requests(self):
#         urls = [
#             # 'https://www.linkedin.com/in/yash-bhavsar-a62630208',
#             'https://www.nseindia.com/', 

#         ]
#         for url in urls:
#             user_agent = next(self.user_agents)
#             headers = {
#                 "User-Agent": user_agent
#             }
#             yield SplashRequest(url, self.parse_result, args={'wait': 10}, headers=headers)

#     def parse_result(self, response):
#         xpath_query="abc"
#         item = {}
#         for selector in self.selectors:
#             elements = response.css(selector)
#             if elements:
#                 self.logger.info(f"Data from elements matching selector '{selector}':")
#                 item[selector] = [element.xpath('string()').get().strip() for element in elements]
#             elif selector=="href":
#                 item['text']=response.xpath('//a//text()').getall()
#                 item['links'] = response.xpath('//a/@href').getall()      
                
#             elif selector=="profile":
#                 description=response.xpath('/*[@id="profile-content"]/div/div[2]/div/div/main/section[5]/div[3]/div/div/div/span[2]').get()
#                 if description:
#                     self.logger.info(f"Description extracted: '{description}'")
#                     item['description'] = description.strip()
#                     self.save_to_text(description.strip())  # Saving description to text file
#             else:
#                 self.logger.warning("Description element not found.")
              
              
                
#                 for selector in self.selectors:

#                       if selector.startswith('#'):  
#                            table_id = selector[1:]  
#                            xpath_query = f'//*[@id="[{table_id}]"]'
#                       elif selector.startswith('.'):  
#                           class_name = selector[1:]  
#                           xpath_query = f'//table[contains(concat(" ", normalize-space(@class), " "), " {class_name} ")]'
#                       else:
#                           self.logger.warning(f"Unsupported selector type: '{selector}'")
#                           continue

#             tables = response.xpath(xpath_query)
#             for table in tables:
#                item = {}
#                rows = table.xpath('.//tr')
#                for row in rows[1:]:
#                   cells = row.xpath('.//td//text()').extract()
#                   if cells:
#                       item['table'] = selector
#                       item['values'] = [cell.strip() for cell in cells if cell.strip()]
#                       self.results.append(item)

#         self.results.append(item)

#     def closed(self, reason):
#         self.save_to_csv(self.results)

#     def save_to_csv(self, results):
#         try:
#             if results:
#                 with open('description.csv', 'w', newline='', encoding='utf-8') as csvfile:
#                     writer = csv.writer(csvfile)

#                     writer.writerow(["Selector", "Value"])
#                     for result in results:
#                         for key, value in result.items():
#                             if isinstance(value, list) and all(isinstance(item, list) for item in value):

#                                 flattened_values = [sub_item for sublist in value for sub_item in sublist]

#                                 unique_values = list(set(flattened_values))
#                                 for val in unique_values:
#                                     writer.writerow([key, val])
#                             else:
#                                 writer.writerow([key, value])
#                 self.logger.info("Scraped data saved to 'table.csv'.")
#             else:
#                 self.logger.warning("No data to save to CSV.")
#         except Exception as e:
#             self.logger.error(f"Error saving scraped data to Csv")

#     def save_to_text(self, description):
#         try:
#             with open('description.txt', 'w', encoding='utf-8') as text_file:
#                 text_file.write(description)
#             self.logger.info("Description saved to 'description.txt'.")
#         except Exception as e:
#             self.logger.error(f"Error saving description to text file: {e}")
