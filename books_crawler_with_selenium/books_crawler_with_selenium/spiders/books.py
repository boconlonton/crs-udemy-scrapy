from time import sleep

from scrapy import Spider
from scrapy import Request

from scrapy.selector import Selector

from selenium import webdriver

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from books_crawler_with_selenium.items import BooksCrawlerWithSeleniumItem


class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']

    def start_requests(self):
        self.driver = webdriver.Chrome('/home/tan/Downloads/chromedriver_linux64/chromedriver')
        self.driver.get('http://books.toscrape.com')

        sel = Selector(text=self.driver.page_source)
        books = sel.xpath('//h3/a/@href').extract()

        for book in books:
            url = f'https://books.toscrape.com/{book}'
            yield Request(url, callback=self.parse)

        while True:
            try:
                next_page = self.driver.find_element(by=By.XPATH, value='//a[text()="next"]')
                sleep(3)
                self.logger.info('Sleeping for 3 seconds...')
                next_page.click()

                # Extracting next page
                sel = Selector(text=self.driver.page_source)
                books = sel.xpath('//h3/a/@href').extract()
                for book in books:
                    url = f'https://books.toscrape.com/catalogue/{book}'
                    yield Request(url, callback=self.parse)
            except NoSuchElementException:
                self.logger.info('No more pages to load...')
                self.driver.quit()
                break

    def parse(self, response, **kwargs):
        items = BooksCrawlerWithSeleniumItem()
        title = response.css('h1::text').extract_first()
        url = response.request.url

        items['title'] = title
        items['url'] = url
        yield items
