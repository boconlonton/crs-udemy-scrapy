from scrapy import Spider

from scrapy.http import Request


class JobsSpider(Spider):
    name = 'jobs'
    allowed_domains = ['newyork.craigslist.org']
    start_urls = ['https://newyork.craigslist.org/search/egr/']

    def parse(self, response, **kwargs):
        results = response.xpath('//*[@class="result-row"]')
        for record in results:
            date_posted = record.xpath('.//*[@class="result-date"]/@datetime').extract_first()
            title = record.xpath('.//*[contains(@class, "result-title")]/text()').extract_first()
            url = record.xpath('.//*[contains(@class, "result-title")]/@href').extract_first()

            yield Request(url=url,
                          callback=self.parse_job,
                          meta={
                              'date_posted': date_posted,
                              'title': title,
                              'url': url,
                          })

        next_page = response.xpath('//*[@class="button next"]/@href').extract_first()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield Request(url=next_page_url, callback=self.parse)

    def parse_job(self, response, **kwargs):
        date = response.meta['date_posted']
        link = response.meta['url']
        title = response.meta['title']
        compensation = response.xpath('//*[@class="attgroup"]/span[1]/b/text()').extract_first()
        employment_type = response.xpath('//*[@class="attgroup"]/span[2]/b/text()').extract_first()
        images = response.xpath('//*[@id="thumbs"]//@src').extract()
        images = [
            image.replace('50x50c', '600x450')
            for image in images
        ]
        description = response.xpath('//*[@id="postingbody"]/text()').extract()
        yield {
            'date': date,
            'link': link,
            'title': title,
            'compensation': compensation,
            'employment_type': employment_type,
            'images': images,
            'description': description,
        }

