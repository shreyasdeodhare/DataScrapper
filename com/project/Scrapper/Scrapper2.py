import json
from typing import Iterable 
import scrapy
from urllib.parse import urljoin
import re
import csv

class  AScrap(scrapy.Spider): 
    name="asearch"
    def start_requests(self) :
        keyword_list=['ipad']
        for keyword in keyword_list: 
            amazon_search_url=f'https://www.amazon.com/s?k={keyword}&page=1'
            yield scrapy.Request(url=amazon_search_url,callback=self.discover_product_urls,meta={'keyword':keyword,'page':1})
    def discover_product_urls(self, response):
        page = response.meta['page']
        keyword = response.meta['keyword'] 

        ## Discover Product URLs
        search_products = response.css("div.s-result-item[data-component-type=s-search-result]")
        for product in search_products:
            relative_url = product.css("h2>a::attr(href)").get()
            product_url = urljoin('https://www.amazon.com/', relative_url).split("?")[0]
            yield scrapy.Request(url=product_url, callback=self.parse_product_data, meta={'keyword': keyword, 'page': page})
            
        ## Get All Pages
        if page == 1:
            available_pages = response.xpath(
                '//*[contains(@class, "s-pagination-item")][not(has-class("s-pagination-separator"))]/text()'
            ).getall()

            last_page = available_pages[-1]
            for page_num in range(2, int(last_page)):
                amazon_search_url = f'https://www.amazon.com/s?k={keyword}&page={page_num}'
                yield scrapy.Request(url=amazon_search_url, callback=self.parse_search_results, meta={'keyword': keyword, 'page': page_num})

        def parse_product_data(self, response):
          title=response.css('span#producTitle::text').get()
          price=response.css('span#priceblock_outprice::text').get()
          csv_data={
              'keyword': response.meta['keyword'], 
              'title': title.strip() if title else None,
              'price' : price.strip() if price else None, 
              'url' : response.url 
              
          }
          self.write_to_csv(csv_data)
        
        def write_to_csv(self,data): 
            with open('amazon_data.csv','a',newline='',encoding='utf-8') as csvfile: 
                fieldnames=['keyword','title','price','url']
                writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
                if csvfile.tell()==0: 
                    writer.writeheader()
                writer.writerow(data) 
        
        