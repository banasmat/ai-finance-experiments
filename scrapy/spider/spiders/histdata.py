# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
import zipfile, io


class HistdataSpider(scrapy.Spider):
    name = 'histdata'
    allowed_domains = ['histdata.com']

    url_base = 'http://www.histdata.com'
    start_urls = [url_base + '/download-free-forex-data/?/metatrader/1-minute-bar-quotes']


    def parse(self, response):
        links = response.css(".page-content a[href^=\/download-free]::attr(href)").extract()
        for link in links:
            yield scrapy.Request(self.url_base + '/' + link,
                                 self.parse_currency_pair_page)

    def parse_currency_pair_page(self, response):
        links = response.css(".page-content a[href^=\/download-free]::attr(href)").extract()
        for link in links:
            yield scrapy.Request(self.url_base + '/' + link,
                                 self.parse_download_page)

    def parse_download_page(self, response):
        yield FormRequest.from_response(response, formid='file_down', callback=self.get_data)

    def get_data(self, response):
        z = zipfile.ZipFile(io.BytesIO(response.body))
        z.extractall('output')
