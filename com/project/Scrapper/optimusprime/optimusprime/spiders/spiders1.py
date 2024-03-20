import scrapy

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['http://www.nseindia.com']

    def parse(self, response):
        # Extract HTML content
        html_content = response.body_as_unicode()

        # Extract data under <nav> elements with class name 'tabs_boxes'
        relevant_data = self.extract_data_with_xpath(response)

        yield {
            'relevant_data': relevant_data
        }

    def extract_data_with_xpath(self, response):
        # Define XPath expression to find <nav> elements with class name 'tabs_boxes'
        xpath_expression = "//nav[@class='tabs_boxes']//*"

        # Extract data using XPath
        extracted_data = response.xpath(xpath_expression).getall()

        return extracted_data
