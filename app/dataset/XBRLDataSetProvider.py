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

            numbers = pd.read_csv(num_file, sep='\t', encoding='ISO-8859-1')

            # print(numbers['tag'])
            #
            # nazwa taga jeset nieważna
            # ważna jest tylko proporcja w stosunku do poprzednich wpisów z tego samego taga
            #
            # tylko jak wybrać te dobre firmy? jak ustawić labels?
            # labels powinno być tyle ile firm


            revenues = numbers.loc[numbers['tag'] == 'Revenue']
            print(revenues)
            quit()

            tags = numbers['tag'].unique()

            for tag in tags:
                if 'revenue' == tag.lower():
                    print(tag)
            quit()


