from typing import List, Tuple

import numpy as np
import pandas as pd
import os


class XBRLDataSetProvider(object):

    @staticmethod
    def extract_cik_numbers():
        res_dir = os.path.join(os.path.abspath(os.getcwd()), 'scrapy', 'xbrl_output')

        cik_numbers = []

        for quarter_dir in reversed(os.listdir(res_dir)):

            quarter_dir = os.path.join(res_dir, quarter_dir)

            if not os.path.isdir(quarter_dir):
                continue

            sub_file = os.path.join(quarter_dir, 'sub.txt')
            subs = pd.read_csv(sub_file, sep='\t', encoding='ISO-8859-1', usecols=['cik'])

            cik_numbers = list(set(cik_numbers + subs['cik'].tolist()))

        cik_file_path = os.path.join(os.path.abspath(os.getcwd()), 'resources', 'cik.txt')

        with open(cik_file_path, 'w') as f:
            for cik in cik_numbers:
                f.write("%s\n" % cik)

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

