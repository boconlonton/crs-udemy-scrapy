import scrapy

from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/login']

    def parse(self, response, **kwargs):
        csrf_token = response.xpath('//*[@name="csrf_token"]/@value').extract_first()
        yield FormRequest('http://quotes.toscrape.com/login', formdata={
            'csrf_token': csrf_token,
            'username': 'foobar',
            'password': 'foobar',
        }, callback=self.parse_after_login)

    def parse_after_login(self, response, **kwargs):
        # Open new tab
        open_in_browser(response)

        # Assert the result
        # if response.xpath('//a[text()="Logout"]'):
        #     self.log('You logged in')
