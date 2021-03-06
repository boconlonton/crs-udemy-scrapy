import os

import glob

from scrapy import Spider

from scrapy.http import Request


def product_info(response, value):
    return response.xpath(f'//th[text()="{value}"]/following-sibling::td/text()').extract_first()


class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def __init__(self, category, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [category]

    def parse(self, response, **kwargs):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            absolute_url = response.urljoin(book)
            yield Request(url=absolute_url, callback=self.parse_book)

        # process next age
        next_page_url = response.xpath('//a[text()="next"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield Request(url=absolute_next_page_url)

    def parse_book(self, response, **kwargs):
        title = response.xpath('//h1/text()').extract_first()
        price = response.xpath('//*[@class="price_color"]/text()').extract_first()
        image_url = response.xpath('//img/@src').extract_first()
        image_url = image_url.replace('../..', 'http://books.toscrape.com/')
        rating = response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
        rating = rating.replace('star-rating ', '')
        description = response.xpath('//*[@id="product_description"]/following-sibling::p/text()').extract_first()

        # product information
        upc = product_info(response, "UPC")
        product_type = product_info(response, "Product Type")
        price_exclude_tax = product_info(response, "Price (excl. tax)")
        price_include_tax = product_info(response, "Price (incl. tax)")
        tax = product_info(response, "Tax")
        availability = product_info(response, "Availability")
        no_of_reviews = product_info(response, "Number of reviews")
        yield {
            'title': title,
            'price': price,
            'image_url': image_url,
            'rating': rating,
            'description': description,
            'upc': upc,
            'product_type': product_type,
            'price_exclude_tax': price_exclude_tax,
            'price_include_tax': price_include_tax,
            'tax': tax,
            'availability': availability,
            'no_of_reviews': no_of_reviews,
        }

    def close(self, reason):
        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)
        os.rename(csv_file, 'foobar.csv')
