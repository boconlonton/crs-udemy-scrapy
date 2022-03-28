from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from scrapy.linkextractors import LinkExtractor


class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    rules = (
        Rule(LinkExtractor(allow=('music')), callback='parse_page', follow=True),
    )

    def parse_page(self, response, **kwargs):
        yield {
            'URL': response.url
        }
