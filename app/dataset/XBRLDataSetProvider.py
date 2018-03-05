from typing import List, Tuple

import numpy as np
import pandas as pd
import os
import pickle
import csv
from fuzzywuzzy import process

class XBRLDataSetProvider(object):

    titles = {
        # income statement
        'revenue': ['net operating revenues', 'total non-interest revenues'],
        'cost of goods sold': [],
        'gross profit': [],  #
        'selling, general & admin': ['selling, general and administrative expenses'],
        'research & development': ['research', 'research and development'],  # ?
        'interest': ['interest expense'],
        'depreciation': ['depreciation depletion and amortization'],  # ?
        'operating profit': [],  #
        'gain (loss) sale assets': [],
        'other': [],
        'income before tax': ['income before income taxes'],  #
        'income taxes paid': ['income taxes'],
        'net earnings': [],  # !

        # balance sheet
        'cash & short-term investments': [],
        'total inventory': [],
        'total receivables, net': ['AccountsReceivableNetCurrent'],
        'prepaid expenses': [],
        'other current assets, total': [],
        'total current assets': [],  #
        'property/plant/equipment': [],
        'goodwill, net': [],
        'intangibles, net': [],
        'long-term investments': [],
        'other assets': [],
        'total assets': [],  #
        'accounts payable': ['AccountsPayableCurrent', 'AccountsPayableRelatedPartiesCurrent'],
        'accrued expenses': ['AccruedLiabilitiesCurrent'],
        'short-term debt': [],
        'long-term debt due': [],
        'other current liabilities': [],
        'total current liabilities': [],  #
        'long-term debt': [],
        'deferred income tax': [],
        'minority interest': [],
        'other liabilities': [],
        'total liabilities': [],  #
        'preferred stock': [],
        'common stock': [],
        'additional paid in capital': ['AdditionalPaidInCapital'],
        'retained earnings': [],
        'treasury stock-common': [],
        'other equity': [],
        'total shareholders equity': [],  #
        'total liabilities & shareholders equity': [],  #

        # cash flow
        'net income': [],
    #    'depreciation': ['AccumulatedDepreciationDepletionAndAmortizationPropertyPlantAndEquipment'],
        'amortization': [],
        'total cash from operating activities': [],  #
        'capital expenditures': [],
        'other investing cash flow items': [],
        'total cash from investing activities': [],  #
        'cash dividends paid': [],
        'issuance retirement of stock, net': [],
        'issuance retirement of debt, net': [],
        'total cash from financing activities': [],  #
        'net change in cash': [],  #

     #   '?': ['AllowanceForDoubtfulAccountsReceivableCurrent']

    }

    @staticmethod
    def extract_cik_numbers():
        res_dir = os.path.join(os.path.abspath(os.getcwd()), 'scrapy', 'xbrl_output')

        cik_map = {}

        for quarter_dir in reversed(os.listdir(res_dir)):

            quarter_dir = os.path.join(res_dir, quarter_dir)

            if not os.path.isdir(quarter_dir):
                continue

            sub_file = os.path.join(quarter_dir, 'sub.txt')
            subs = pd.read_csv(sub_file, sep='\t', encoding='ISO-8859-1', usecols=['cik', 'name'])

            for index, row in subs.iterrows():
                cik_map[row['cik']] = row['name']

        cik_file_path = os.path.join(os.path.abspath(os.getcwd()), 'resources', 'cik.pkl')

        with open(cik_file_path, 'wb') as f:
            pickle.dump(cik_map, f)

    @staticmethod
    def organize_tags():
        res_dir = os.path.join(os.path.abspath(os.getcwd()), 'scrapy', 'xbrl_output')
        all_tags = pd.Series()

        for quarter_dir in reversed(os.listdir(res_dir)):

            quarter_dir = os.path.join(res_dir, quarter_dir)

            if not os.path.isdir(quarter_dir):
                continue

            tag_file = os.path.join(quarter_dir, 'tag.txt')
            tags = pd.read_csv(tag_file, sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE, usecols=['tag'])
            all_tags = all_tags.append(tags)

        all_tags = all_tags['tag'].unique().tolist()

        # target_file_path = os.path.join(os.path.abspath(os.getcwd()), 'resources', 'tags.txt')
        #
        # with open(target_file_path, 'a') as f:
        #     for item in all_tags:
        #         f.write("%s\n" % item)

        target_file_path = os.path.join(os.path.abspath(os.getcwd()), 'resources', 'tags_organized.txt')

        for title in XBRLDataSetProvider.titles.keys():

            title = title.replace('&', 'and')

            result = process.extract(title, all_tags, limit=15)
            with open(target_file_path, 'a') as f:
                f.write("\n%s:\n" % title)
                for item in result:
                    f.write("%s - %s\n" % (item[0], str(item[1])))

    @staticmethod
    def get_data_set():

        res_dir = os.path.join(os.path.abspath(os.getcwd()), 'scrapy', 'xbrl_output')

        for quarter_dir in reversed(os.listdir(res_dir)):

            quarter_dir = os.path.join(res_dir, quarter_dir)

            if not os.path.isdir(quarter_dir):
                continue

            num_file = os.path.join(quarter_dir, 'num.txt')
            sub_file = os.path.join(quarter_dir, 'sub.txt')

            numbers = pd.read_csv(num_file, sep='\t', encoding='ISO-8859-1', usecols=['adsh', 'tag', 'value'])
            subs = pd.read_csv(sub_file, sep='\t', encoding='ISO-8859-1', usecols=['adsh', 'name'])

            # print(numbers['tag'])
            #
            # nazwa taga jeset nieważna
            # ważna jest tylko proporcja w stosunku do poprzednich wpisów z tego samego taga
            #
            # tylko jak wybrać te dobre firmy? jak ustawić labels?
            # labels powinno być tyle ile firm

            # 1. ile tagów jest reużywanych przez firmy?

            # gdyby każda firma używała każdego taga wyszłoby 733076562 rekordów w num, a jest 2255775 (a często firma używa taga dwa razy dla jednego sprawozdania)
            # Liczba wszystkich użyć tagów podzielona przez liczbę dostępnych tagów to 20 a firm mamy 6506
            # stąd wniosek, że każda firma używa dużo customowych tagów
            # trudno jest utworzyć w ogóle strukturę danych, która pomieści taką ilość tagów
            # nie widzę sensu traktowania taga jako wspólnej jednostki dla różnych firm

            tags = pd.Series(numbers['tag'].unique())
            print(len(subs.index))
            print(len(numbers['tag'])/len(tags))
            quit()
            # data = np.zeros((1, len(tags), 2), dtype={'names': tags, 'formats': ['f4'] * len(tags)})

            df = pd.DataFrame(index=range(0, len(subs.index)), columns=tags, dtype=np.int8)
            df.fillna(0, inplace=True)
            df.index = subs['name']
            # numbers.join(subs, on='adsh')


            print(df.head())
            # print(data)
            print(df.columns)
            print(df.info(memory_usage=True))
            quit()


            revenues = numbers.loc[numbers['tag'] == 'Revenue']
            print(revenues)
            quit()

            tags = numbers['tag'].unique()

            for tag in tags:
                if 'revenue' == tag.lower():
                    print(tag)
            quit()


