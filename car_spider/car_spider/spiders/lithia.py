import scrapy


class LithiaSpider(scrapy.Spider):
    name = 'lithia'
    allowed_domains = ['lithia.com']
    start_urls = ['http://lithia.com/']

    def parse(self, response, **kwargs):
        pass
