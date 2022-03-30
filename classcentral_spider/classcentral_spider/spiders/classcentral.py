from scrapy import Spider

from scrapy.http import Request

from classcentral_spider.items import Subject


class ClasscentralSpider(Spider):
    name = 'classcentral'
    allowed_domains = ['classcentral.com']
    start_urls = ['http://classcentral.com/subjects']

    def __init__(self, subject: str = None, **kwargs):
        super().__init__(**kwargs)
        self.subject = subject

    def parse(self, response, **kwargs):
        if self.subject is not None:
            self.log(f'Scraping for subject: {self.subject}')
            subject_url = response.xpath(
                f'//*[contains(@title, "{self.subject}")]/@href'
            ).extract_first()
            yield Request(url=response.urljoin(subject_url), callback=self.parse_subject)
        else:
            self.log('Scraping all subjects.')
            subjects = response.xpath('//h3/a[1]/@href').extract()
            for subject in subjects:
                yield Request(url=response.urljoin(subject), callback=self.parse_subject)

    def parse_subject(self, response, **kwargs):
        subject_name = response.xpath('//h1/text()').extract_first()
        courses = response.xpath('//li[@itemtype="http://schema.org/Event"]')
        for course in courses:
            item = Subject()
            item['name'] = course.xpath('.//h2[@itemprop="name"]/text()').extract_first().strip()
            item['apply_url'] = course.xpath('.//*[@class="color-charcoal course-name"]/@href').extract_first()
            item['description'] = course.xpath(
                './/*[@class="color-charcoal block hover-no-underline break-word"]/text()').extract_first()
            item['work_load'] = course.xpath('.//*[@aria-label="Workload and duration"]/text()').extract_first()
            item['start_date'] = course.xpath('.//*[@itemprop="startDate"]/@content').extract_first()
            item['pricing'] = course.xpath('.//*[@aria-label="Pricing"]/text()').extract_first()
            item['subject'] = subject_name
            yield item

        next_page_url = response.xpath('//link[@rel="next"]/@href').extract_first()
        if next_page_url:
            yield Request(response.urljoin(next_page_url), callback=self.parse_subject)
