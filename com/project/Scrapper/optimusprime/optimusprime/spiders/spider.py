import scrapy
import csv
import scrapy_fake_useragent

class NSEIndicesSpider(scrapy.Spider):
    name = "nse_indices"
    start_urls = ["https://www.nseindia.com"]  # Replace with the actual URL
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_DEBUG': True,
        'DOWNLOAD_DELAY': 1,
        'DEPTH_LIMIT': 1,
    }

    def parse(self, response):
        indices = []

        for tab in response.css('.nav-tabs .nav-item'):
            index_data = {}
            index_data['symbol'] = tab.css('p.tb_name::text').get()
            index_data['value'] = tab.css('p.tb_val::text').get()
            index_data['change'] = tab.css('p.tb_per::text').get()

            indices.append(index_data)

        if not indices:
            self.log("No indices found!")

        # Write data to CSV file
        csv_file = 'nse_indices_data.csv'
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['symbol', 'value', 'change']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(indices)

        self.log(f"Data has been written to {csv_file}")
