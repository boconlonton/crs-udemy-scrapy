from scrapy import Spider

from scrapy.http import Request
from scrapy.http import FormRequest


class EplanningSpider(Spider):
    name = 'eplanning'
    allowed_domains = ['eplanning.ie']
    start_urls = ['http://eplanning.ie/']

    def parse(self, response, **kwargs):
        urls = response.xpath('//a/@href').extract()
        for url in urls[0:1]:
            if '#' == url:
                pass
            else:
                yield Request(url=url, callback=self.parse_application)

    def parse_application(self, response):
        app_url = response.xpath('//*[@class="glyphicon glyphicon-inbox btn-lg"]/following-sibling::a/@href').extract_first()
        yield Request(url=response.urljoin(app_url), callback=self.parse_form)

    def parse_form(self, response):
        yield FormRequest.from_response(response=response,
                                        formdata={
                                            'RdoTimeLimit': '42',
                                        },
                                        dont_filter=True,
                                        formxpath='(//form)[2]',
                                        callback=self.parse_pages)

    def parse_pages(self, response):
        application_urls = response.xpath('//td/a/@href').extract()
        for url in application_urls:
            url = response.urljoin(url)
            yield Request(url, callback=self.parse_items)
        next_page_url = response.xpath('//*[@rel="next"]/@href').extract_first()
        if next_page_url:
            yield Request(url=response.urljoin(next_page_url), callback=self.parse_pages)

    def parse_items(self, response):
        agent_btn = response.xpath('//input[@title="Show Agents Popup"]/@style').extract_first()
        if 'display: inline;  visibility: visible;' in agent_btn:
            name = response.xpath('//tr[th="Name :"]/td/text()').extract_first()
            adr = " ".join(response.xpath('//tr[th="Address :"]/following-sibling::tr/td/text()').extract()[:3])

            phone = response.xpath('//tr[th="Phone :"]/td/text()').extract_first()
            fax = response.xpath('//tr[th="Fax :"]/td/text()').extract_first()
            email = response.xpath('//tr[th="e-mail :"]/td/a/text()').extract_first()
            email = email.strip() if email else email
            url = response.url
            yield {
                'name': name,
                'address': adr,
                'phone': phone,
                'fax': fax,
                'email': email,
                'url': url
            }
        else:
            self.logger.info('Agent button not found on page,, passing invalid url.')

