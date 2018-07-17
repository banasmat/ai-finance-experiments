# -*- coding: utf-8 -*-
import scrapy
import zipfile, io, os, csv
import pandas as pd


class YahooFinanceSpider(scrapy.Spider):
    name = 'yahoo_finance'
    allowed_domains = ['yahoo.com']

    url_base = 'https://finance.yahoo.com/quote/'
    start_urls = []

    cik_map_file_path = os.path.join(os.path.abspath(os.getcwd()), '..', 'output', 'cik_map_precise.csv')

    def __init__(self, name=None, **kwargs):

        super().__init__(name, **kwargs)

        df = pd.read_csv(self.cik_map_file_path, usecols=['symbol'])
        all_symbols = df.symbol.tolist()

        for symbol in all_symbols[:1]:
            self.start_urls.append(self.url_base + symbol + '/financials?p=' + symbol)
            self.start_urls.append(self.url_base + symbol + '/balance-sheet?p=' + symbol)
            self.start_urls.append(self.url_base + symbol + '/cash-flow?p=' + symbol)

    def parse(self, response: scrapy.http.response.Response):
        #TODO
        # get data
        # save to file

        data = response.css("[data-test=qsp-financial] tbody").extract()