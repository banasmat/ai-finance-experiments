# -*- coding: utf-8 -*-
import scrapy, datetime, csv
import zipfile, io, pickle, os, re


class FinancialStatementSpider(scrapy.Spider):
    name = 'financial_statement'
    allowed_domains = ['sec.gov']

    url_base = 'https://www.sec.gov'
    start_urls = []

    cik_map = {}

    output_dir = os.path.join(os.path.abspath(os.getcwd()), '..', 'resources', 'financial_statements')

    def __init__(self, **kwargs):

        cik_file_path = os.path.join(os.path.abspath(os.getcwd()), '..', 'resources', 'cik.pkl')

        with open(cik_file_path, 'rb') as f:
            self.cik_map = pickle.load(f)

        for cik in list(self.cik_map.keys())[:10]:
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

        document_type = response.css('th.tl strong').extract_first()
        period_label = response.css('th.th::text').extract_first()
        dt = response.css('th.th div::text').extract_first()

        if period_label is None or document_type is None or dt is None:
            # print(period_label)
            # print(document_type)
            # print(dt)
            return

        document_type = document_type.lower()
        period_label = period_label.lower()

        period_labels = ['12 months ended']
        document_types = {
            'income_statement': 'consolidated statements of income',
            'balance_sheet': 'consolidated balance sheets',
            'cash_flow': 'consolidated statements of cash flows'
        }

        is_period_important = False
        is_document_important = False

        for p_label in period_labels:
            if p_label in period_label:
                is_period_important = True
                break

        for slug, d_type in document_types.items():
            if d_type in document_type:
                is_document_important = True
                break

        if is_period_important and is_document_important:
            if "thousand" in document_type:
                multiplier = 1000
            elif "million" in document_type:
                multiplier = 1000000
            elif "billion" in document_type:
                multiplier = 1000000000
            else:
                raise RuntimeError('No multiplier defined in ' + response.url + '. Document heading: ' + document_type)

            year = dt[-4:]
            cik = response.url.rsplit('/')[-3]

            fin_dict = {'cik': cik}

            records = response.css('tr')
            for record in records:
                record_title = record.css('td.pl a::text').extract_first()
                if record_title:
                    record_title = record_title.replace(',', '')
                    value = record.css('td.nump::text').extract_first()
                    # print(record_title, value)
                    if value:
                        digit_val = re.findall(r'[\d+,]+', value)[0]
                        # print('digit_val', digit_val)
                        if digit_val:
                            digit_val = float(digit_val.replace(',', '.')) * multiplier
                            fin_dict[record_title] = str(digit_val)

            file_path = os.path.join(self.output_dir, year + '.csv')
            mode = 'w'
            if os.path.isfile(file_path):
                mode = 'a'
            with open(file_path, mode) as f:
                print('Saving output to ' + file_path)
                #FIXME sort before saving
                w = csv.DictWriter(f, fin_dict.keys())
                # if mode == 'w':
                w.writeheader()
                w.writerow(fin_dict)
        else:
            pass
            # print('IGNORING DOCUMENT: ' + response.url)