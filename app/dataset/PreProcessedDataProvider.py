from typing import List
import pandas as pd
import os
import numpy as np
import pickle


class PreProcessedDataProvider(object):
    res_dir = 'resources/'
    price_res_dir = 'resources/oanda_prices/'
    scale_map = {}

    @staticmethod
    def get_currency_pair_strings() -> List:
        pairs = []
        for filename in os.listdir(PreProcessedDataProvider.price_res_dir):
            if filename.endswith('.csv'):
                pairs.append(filename[:-4])

        return pairs

    def get_currency_pairs(self) -> np.chararray:

        pairs_len = len([filename for filename in os.listdir(self.price_res_dir) if filename.endswith('.csv')])
        pairs = np.chararray((pairs_len, 2), itemsize=3, unicode=True)
        i = 0

        for filename in os.listdir(self.price_res_dir):
            if filename.endswith('.csv'):
                fname = filename[:-4]
                pairs[i][0] = fname[:-3]
                pairs[i][1] = fname[3:]
                i += 1

        return pairs

    def get_all_currencies(self):
        return list(set(self.get_currency_pairs().flatten().tolist()))

    def get_price_data(self, symbol_1: str, symbol_2: str) -> pd.DataFrame:
        prices = self.get_price_records(symbol_1, symbol_2, ('datetime', 'high', 'low'))
        prices['mean'] = (pd.to_numeric(prices.pop('high')) + pd.to_numeric(prices.pop('low'))) / 2

        return prices

    def get_price_records(self, symbol_1, symbol_2, usecols=('datetime', 'finished', 'open', 'high', 'low', 'close', 'volume'), gran='H1'):

        col_indexes = []
        all_cols=['datetime', 'finished', 'open', 'high', 'low', 'close', 'volume']
        for col in usecols:
            col_indexes.append(all_cols.index(col))

        prices = pd.read_csv(self.price_res_dir + symbol_1 + symbol_2 + '.csv', sep=',', usecols=col_indexes)
        prices.columns = usecols

        if 'datetime' in prices.columns:
            prices.index = pd.to_datetime(prices.pop('datetime').astype(str), format='%Y-%m-%dT%H:%M:%S')

        if gran == 'D1':
            prices = prices.resample('1D').mean()
            prices.dropna(inplace=True)

        return prices

    def get_news_data(self, from_datetime: pd.Timestamp, symbol_1: str, symbol_2: str) -> pd.DataFrame:

        news = pd.read_csv(self.res_dir + 'forex-news.csv', sep=';', dtype=str,
                           usecols=('date', 'time', 'symbol', 'title', 'actual', 'forecast', 'previous'))

        news = news.loc[news['symbol'].isin([symbol_1, symbol_2]) & news['time'].str.contains('^\d{2}:')]

        news['datetime'] = pd.to_datetime(news.pop('date') + news.pop('time'), format='%Y-%m-%d%H:%M')
        news = news.loc[news['datetime'] >= from_datetime]

        news['symbol_pair'] = symbol_1 + symbol_2

        for key in ['actual', 'forecast', 'previous']:
            news[key] = news[key].apply(self.normalize_numeric_string_value)
            news.apply(lambda row: self.__update_scale_map(row, key), axis=1)

        news = news.loc[~news['actual'].isnull()]

        # reversing order
        # news = news.iloc[::-1]

        return news

    def scale_news_data(self, news: pd.DataFrame) -> pd.DataFrame:

        # Rounding to previous hour - now we don't need 1M price data, but 1H TODO news timezone seems to me ok (utc) how about training prices???
        news['datetime'] = news.apply(lambda row: row['datetime'].replace(microsecond=0, second=0, minute=0), axis=1)

        news = news.loc[news['title'].isin(self.get_all_titles())]

        for key in ['forecast', 'previous', 'actual']:
            self.scale_map[key] = dict(map(self.__reduce_to_min_and_max, self.scale_map[key].items()))
            news = news.apply(lambda row: self.__scale_values(row, key), axis=1)

        # self.scale_map['actual'] = dict(map(self.__reduce_to_min_and_max, self.scale_map['actual'].items()))
        # news = news.apply(lambda row: self.__scale_values(row, 'actual', 10), axis=1)

        return news

    def get_all_titles(self) -> List:
        return list(self.scale_map['actual'].keys())

    def save_scale_map(self):
        with open('output/scale_map.pkl', 'wb') as f:
            pickle.dump(self.scale_map, f)

    def load_scale_map(self):
        if not self.scale_map:
            with open('output/scale_map.pkl', 'rb') as f:
                self.scale_map = pickle.load(f)

    @staticmethod
    def normalize_numeric_string_value(val):

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

        if row['title'] not in self.scale_map[key]:
            print('x')
            return None

        if row[key] is None:
            scaled = 0
        else:
            scaled = row[key] - self.scale_map[key][row['title']][0]
            scaled /= self.scale_map[key][row['title']][1] - self.scale_map[key][row['title']][0]
            scaled *= max_value

        if scaled > max_value:
            # TODO check why in two cases row['actual'] is larger than previously counted max
            scaled = max_value

        row[key] = float("{0:.2f}".format(scaled * 10))

        return row
