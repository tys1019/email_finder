import argparse
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
from selenium import webdriver
from urlparse import urlparse

class EmailSpider(CrawlSpider):
    name = "emailspider"

    emails = set()

    def __init__(self, category=None, *args, **kwargs):
        self.driver = webdriver.PhantomJS(service_args=['--load-images=no'])
        super(CrawlSpider, self).__init__(*args, **kwargs)

    def __del__(self):
        self.driver.quit()

    def parse(self, response):
        sel = Selector(response)
        for url in sel.xpath('//a/@href').extract():
            if url.startswith('mailto:'):
                self.emails.add(url.replace('mailto:', ''))

            elif url.startswith('http'):
                if urlparse(url).netloc != self.DOMAIN:
                    continue

            else:
                url = self.DOMAIN_URL.format(url)

            yield Request(url, callback=self.parse)

        # Doesn't load Javascript data
        # for ng_click in sel.xpath('//@ng-click').extract():
        #     if 'changeRoute' in ng_click:
        #         path = ng_click.replace("changeRoute('", '').replace("')", '')
        #         url = DOMAIN_URL.format(path)
        #         yield Request(url, callback=self.parse)


def run_spider(DOMAIN):
    DOMAIN_URL = "http://{}/{}".format(DOMAIN, {})
    EmailSpider.allowed_domains = [DOMAIN]
    EmailSpider.start_urls = [DOMAIN_URL.format('')]
    EmailSpider.DOMAIN_URL = DOMAIN_URL
    EmailSpider.DOMAIN = DOMAIN

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(EmailSpider)
    process.start()
    print u"Found these email addresses:\n{}".format('\n'.join(EmailSpider.emails))
