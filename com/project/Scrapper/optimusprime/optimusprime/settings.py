import scrapeops_scrapy_proxy_sdk
import scrapy_fake_useragent

BOT_NAME = 'lpp'

SPIDER_MODULES = ['optimusprime.spiders']
NEWSPIDER_MODULE = 'optimusprime.spiders'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 100
CONCURRENT_REQUESTS_PER_DOMAIN = 50


SCRAPEOPS_API_KEY = '657a346b-bcd5-4e50-bbc8-5c9db8514a71'
SCRAPEOPS_PROXY_ENABLED = True
SCRAPEOPS_PROXY_SETTINGS = {'country':'in'}  

EXTENSIONS = {
    'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500,
}

DOWNLOADER_MIDDLEWARES = {
    'scrapeops_scrapy.middleware.retry.RetryMiddleware': 725,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
     
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}

FEED_EXPORT_ENCODING = 'utf-8'
