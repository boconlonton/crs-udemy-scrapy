# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Subject(scrapy.Item):
    name = scrapy.Field()
    apply_url = scrapy.Field()
    description = scrapy.Field()
    work_load = scrapy.Field()
    start_date = scrapy.Field()
    pricing = scrapy.Field()
    subject = scrapy.Field()
