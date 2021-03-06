# -*- coding: utf-8 -*-
import scrapy
import zipfile, io


class XBRLSpider(scrapy.Spider):
    name = 'xbrl'
    allowed_domains = ['sec.gov']

    url_base = 'https://www.sec.gov'
    start_urls = [url_base + '/dera/data/financial-statement-data-sets.html']

    def parse(self, response: scrapy.http.response.Response):
        links = response.css(".list a[href^=\/files\/dera\/data\/financial-statement-data-sets\/]::attr(href)").extract()
        for link in links:
            yield scrapy.Request(self.url_base + link,
                                 self.get_data)

    def get_data(self, response: scrapy.http.response.Response):
        z = zipfile.ZipFile(io.BytesIO(response.body))
        target_dir = response.url.rsplit('/', 1)[-1]
        target_dir = target_dir.split('.', 1)[0]
        z.extractall('xbrl_output/' + target_dir)
