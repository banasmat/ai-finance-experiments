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
    target_dir = os.path.join(os.path.abspath(os.getcwd()), '..', 'output', 'yahoo_fundamentals')

    def __init__(self, name=None, **kwargs):

        super().__init__(name, **kwargs)

        with open(os.path.join(os.path.abspath(os.getcwd()), '..', 'yahoo_counter.txt'), "r") as f:
            counter = f.read()
        counter = int(counter)

        df = pd.read_csv(self.cik_map_file_path, usecols=['symbol'])
        symbols = df.symbol.tolist()[counter:counter+1]

        for symbol in symbols:
            print(symbol)
            if os.path.isfile(os.path.join(YahooFinanceSpider.target_dir, symbol + '.csv')):
                counter += 1
                continue
            self.start_urls.append(self.url_base + symbol + '/financials?p=' + symbol)
            self.start_urls.append(self.url_base + symbol + '/balance-sheet?p=' + symbol)
            self.start_urls.append(self.url_base + symbol + '/cash-flow?p=' + symbol)
            counter += 1

        with open(os.path.join(os.path.abspath(os.getcwd()), '..', 'yahoo_counter.txt'), "w") as f:
            f.write(str(counter))

    def parse(self, response: scrapy.http.response.Response):

        base_css = "[data-test=qsp-financial] tbody "

        datetimes = response.css(base_css + 'tr:first-child td:not(:first-child) span::text').extract()
        labels = response.css(base_css + 'tr:not(:first-child) td:first-child:not([colspan]) span::text').extract()
        values = response.css(base_css + 'tr:not(:first-child) td:not(:first-child) ::text').extract()

        datetimes = list(map(lambda x: x.replace('/', '-'), datetimes))

        symbol = response.request.url.split('=')[1]
        target_file = os.path.join(YahooFinanceSpider.target_dir, symbol + '.csv')

        current_label_index = -1
        current_datetime_index = -1
        datetimes_len = len(datetimes)

        df = pd.DataFrame(index=labels, columns=datetimes)
        pd.options.mode.chained_assignment = None

        for i in range(0, len(values)):

            current_datetime_index += 1
            if i % datetimes_len == 0:
                current_label_index += 1
                current_datetime_index = 0

            val = str(values[i]).replace('-', '')
            val = str(val).replace(',', '')
            if str(val) != '':
                val = int(float(val) * 1000) #TODO check if all numbers are in thousands

            df.loc[labels[current_label_index]][datetimes[current_datetime_index]] = val

        mode = 'w'
        header = True
        if os.path.isfile(target_file):
            mode = 'a'
            header = False

        if df.shape[0] != 0 and df.shape[1] != 0:
            with open(target_file, mode) as f:
                df.to_csv(f, header=header)

    # Bypassing 'privacy policy/accept cookies' page
    def make_requests_from_url(self, url):
        request = super(YahooFinanceSpider, self).make_requests_from_url(url)
        request.cookies['BX'] = 'dd1vpm1dkv6ve&b=3&s=i2'
        request.cookies['GUC'] = 'AQABAQFbUOVcIkIhcQTU&s=AQAAAHJpqZ2w&g=W0-b-A'
        return request