# -*- coding: utf-8 -*-
import scrapy
import zipfile, io, pickle, os, re


class FinancialStatementSpider(scrapy.Spider):
    name = 'financial_statement'
    allowed_domains = ['sec.gov']

    url_base = 'https://www.sec.gov'
    start_urls = []

    cik_map = {}

    def __init__(self, **kwargs):

        cik_file_path = os.path.join(os.path.abspath(os.getcwd()), '..', 'resources', 'cik.pkl')

        with open(cik_file_path, 'rb') as f:
            self.cik_map = pickle.load(f)

        for cik in list(self.cik_map.keys())[:1]:
            self.start_urls.append(self.url_base + '/Archives/edgar/data/' + str(cik))

        super().__init__(**kwargs)

    def parse(self, response: scrapy.http.response.Response):

        links = response.css("#main-content a::attr(href)").extract()
        for link in links:
            yield scrapy.Request(self.url_base + link,
                                 self.parse_subpage)

    def parse_subpage(self, response: scrapy.http.response.Response):
        links = response.css("#main-content a::attr(href)").extract()

        for link in links:

            filename = link.rsplit('/', 1)[-1]

            pattern = re.compile("^R\d+\.htm$")
            if pattern.match(filename):
                yield scrapy.Request(self.url_base + link,
                                     self.get_data)

    def get_data(self, response: scrapy.http.response.Response):


        title = response.css('th.tl strong::text').extract_first()

        if "consolidated statements of income" in title:
            if "thousand" in title:
                unit = 'k'
            elif "million" in title:
                unit = 'm'
            elif "billion" in title:
                unit = 'b'

            dates = response.css('tr th div::text').extract_first()

            records = response.css('tr')
            for record in records:
                record_title = record.css('td.pl a::text').extract()
                if record_title == 'Cost of goods sold':
                    values = record.css('td.nump::text').extract()
                    print('---DATES---', dates)
                    print('---VALUES---', values)
                    quit('XXXXXXXXXXXXXXXXXXXXXX')

        target_dir = response.url.rsplit('/')[-3]

        #Scrape:
        '''
        
        Revenue
            Cost of Goods Sold
            Gross Profit
        Operating Expenses
            Selling, General & Admin.
            Research & Development
            Deprecation
            
            
        '''



        # z.extractall('financial_statement_output/' + target_dir)
