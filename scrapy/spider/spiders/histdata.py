# -*- coding: utf-8 -*-
import scrapy
from spider.items import CurrencyPair


class HistdataSpider(scrapy.Spider):
    name = 'histdata'
    allowed_domains = ['histdata.com']

    url_base = 'http://www.histdata.com'
    start_urls = [url_base + '/download-free-forex-data/?/metatrader/1-minute-bar-quotes']

    def parse(self, response):
        links = response.css(".page-content a[href^=\/download-free]::attr(href)").extract()
        for link in links:
            print(link)
            yield scrapy.Request(self.url_base + '/' + link,
                                 self.parse_currency_pair_page)

    def parse_currency_pair_page(self, response):
        name = response.url[-6:]
        file_urls = response.css(".page-content a[href^=\/download-free]::attr(href)").extract()
        yield CurrencyPair(name=name, file_urls=file_urls)
