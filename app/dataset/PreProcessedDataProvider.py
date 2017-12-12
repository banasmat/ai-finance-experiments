from typing import List
import pandas as pd
import os
import numpy as np
import pickle


class PreProcessedDataProvider(object):
    res_dir = 'resources/'
    price_res_dir = 'resources/prices/'
    scale_map = {}

    @staticmethod
    def get_symbol_pair_strings() -> List:
        pairs = []
        for filename in os.listdir(PreProcessedDataProvider.price_res_dir):
            if filename.endswith('.txt'):
                pairs.append(filename[:-4])

        return pairs

    def get_symbol_pairs(self) -> np.chararray:

        pairs_len = len([filename for filename in os.listdir(self.price_res_dir) if filename.endswith('.txt')])
        pairs = np.chararray((pairs_len, 2), itemsize=3, unicode=True)
        i = 0

        for filename in os.listdir(self.price_res_dir):
            if filename.endswith('.txt'):
                fname = filename[:-4]
                pairs[i][0] = fname[:-3]
                pairs[i][1] = fname[3:]
                i += 1

        return pairs

    def get_price_data(self, symbol_1: str, symbol_2: str) -> pd.DataFrame:

        prices = pd.read_csv(self.price_res_dir + symbol_1 + symbol_2 + '.txt', sep=',', dtype=str,
                             usecols=('<DTYYYYMMDD>', '<TIME>', '<HIGH>', '<LOW>'))
        prices.index = pd.to_datetime(prices.pop('<DTYYYYMMDD>').astype(str) + prices.pop('<TIME>').astype(str), format='%Y%m%d%H%M%S')
        prices['mean'] = (pd.to_numeric(prices.pop('<HIGH>')) + pd.to_numeric(prices.pop('<LOW>'))) / 2
        prices = prices['mean'].resample('1H').mean()

        return prices

    def get_news_data(self, from_datetime: pd.Timestamp, symbol_1: str, symbol_2: str) -> pd.DataFrame:

        news = pd.read_csv(self.res_dir + 'forex-news.csv', sep=';', dtype=str,
                           usecols=('date', 'time', 'symbol', 'title', 'actual', 'forecast', 'previous'))

        news = news.loc[news['symbol'].isin([symbol_1, symbol_2]) & news['time'].str.contains('^\d{2}:')]

        news['datetime'] = pd.to_datetime(news.pop('date') + news.pop('time'), format='%Y-%m-%d%H:%M')
        news = news.loc[news['datetime'] >= from_datetime]

        news['symbol_pair'] = symbol_1 + symbol_2

        for key in ['actual', 'forecast', 'previous']:
            news[key] = news[key].apply(self.__normalize_numeric_string_value)
            news.apply(lambda row: self.__update_scale_map(row, key), axis=1)

        news = news.loc[~news['actual'].isnull()]

        # reversing order
        news = news.iloc[::-1]

        return news

    def scale_news_data(self, news: pd.DataFrame) -> pd.DataFrame:

        for key in ['forecast', 'previous']:
            self.scale_map[key] = dict(map(self.__reduce_to_min_and_max, self.scale_map[key].items()))
            news = news.apply(lambda row: self.__scale_values(row, key), axis=1)

        self.scale_map['actual'] = dict(map(self.__reduce_to_min_and_max, self.scale_map['actual'].items()))
        news = news.apply(lambda row: self.__scale_values(row, 'actual', 10), axis=1)

        return news

    def get_all_titles(self) -> List:
        return list(self.scale_map['actual'].keys())

    def save_scale_map(self):
        with open('output/scale_map.pkl', 'wb') as f:
            pickle.dump(self.scale_map, f)

    def load_scale_map(self):
        with open('output/scale_map.pkl', 'rb') as f:
            self.scale_map = pickle.load(f)

    @staticmethod
    def __normalize_numeric_string_value(val):

        val = str(val)

        try:

            if val == '' or val in ['Pass']:
                raise ValueError('Value is empty')
            elif 'K' in val:
                val = val.replace('K', '')
                val = float(val) * 10 ** 3
            elif 'M' in val:
                val = val.replace('M', '')
                val = float(val) * 10 ** 6
            elif 'B' in val:
                val = val.replace('B', '')
                val = float(val) * 10 ** 9
            elif 'T' in val:
                val = val.replace('T', '')
                val = float(val) * 10 ** 12
            elif '%' in val:
                val = val.replace('%', '')
                val = val.replace('<', '')
                val = float(val) / 100
            elif '|' in val:
                # TODO not sure if mean is the best approach here
                actual_vals = val.split('|')
                val = (float(actual_vals[0]) + float(actual_vals[1])) / 2
            else:
                val = float(val)

        except ValueError:
            return None

        return val

    def __update_scale_map(self, row, key):

        if np.math.isnan(row['actual']):
            return

        if key not in self.scale_map.keys():
            self.scale_map[key] = {}

        if row['title'] not in self.scale_map[key].keys():

            self.scale_map[key][row['title']] = []

        self.scale_map[key][row['title']].append(row[key])

    @staticmethod
    def __reduce_to_min_and_max(values):
        _min = min(values[1])
        _max = max(values[1])
        if _min == _max:
            _min -= 1
            _max += 1

        return values[0], [_min, _max]

    def __scale_values(self, row, key, max_value=1):
        scaled = row[key] - self.scale_map[key][row['title']][0]
        scaled /= self.scale_map[key][row['title']][1] - self.scale_map[key][row['title']][0]
        scaled *= max_value

        if scaled > max_value:
            # TODO check why in two cases row['actual'] is larger than previously counted max
            scaled = max_value

        row[key] = float("{0:.2f}".format(scaled * 100))

        return row
