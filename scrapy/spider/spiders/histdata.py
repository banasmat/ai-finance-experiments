# -*- coding: utf-8 -*-
import scrapy
from io import StringIO


class HistdataSpider(scrapy.Spider):
    name = 'histdata'
    allowed_domains = ['histdata.com']

    url_base = 'http://www.histdata.com'
    start_urls = [url_base + '/download-free-forex-data/?/metatrader/1-minute-bar-quotes']

    def parse(self, response):
        yield scrapy.Request(self.url_base + '/'
                             + response.css(".page-content a[href^=\/download-free]::attr(href)").extract_first(),
                             self.parse_currency_pair_page)

    def parse_currency_pair_page(self, response):
        yield scrapy.Request(
            self.url_base + '/' + response.css(".page-content a[href^=\/download-free]::attr(href)").extract_first(),
            self.download_zip)

    def download_zip(self, response):

        with open('test.zip', 'wb') as f:
            f.write(response.body)
        print('tutaj', response)
        quit()

