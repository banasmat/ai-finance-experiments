from typing import List, Tuple

import numpy as np
import pandas as pd
import os


class XBRLDataSetProvider(object):



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

            tags = numbers['tag'].unique()

            df = pd.DataFrame(index=range(0, len(numbers.index)-1), columns=tags)
            df.fillna(0, inplace=True)
            tags.join(subs, on='adsh')


            print(df.head())

            print(df.columns)
            quit()


            revenues = numbers.loc[numbers['tag'] == 'Revenue']
            print(revenues)
            quit()

            tags = numbers['tag'].unique()

            for tag in tags:
                if 'revenue' == tag.lower():
                    print(tag)
            quit()


