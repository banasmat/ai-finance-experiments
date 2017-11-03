import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from collections import Counter


class ForexAnalyzer(object):

    res_dir = 'resources/'

    news_symbols = []
    news_titles = []
    scale_map = {}

    def __init__(self):
        self.get_data()

    def get_data(self):

        def normalize_news_row(row):
            try:
                row['symbol'] = get_news_symbol(row)
                row['title'] = get_news_title(row)
                row['actual'] = get_actual_value(row)
                update_scale_map(row)
            except ValueError:
                return None

            return row

        def get_news_symbol(row):
            return self.news_symbols.index(row['symbol'])

        def get_news_title(row):
            return self.news_titles.index(row['title']) #TODO consider using a one_hot array

        def get_actual_value(row):

            actual_val = row['actual']

            if actual_val == '' or actual_val in ['Pass']:
                raise ValueError('News Actual value is empty')
            elif 'K' in actual_val:
                actual_val = actual_val.replace('K', '')
                actual_val = float(actual_val) * 10**3
            elif 'M' in actual_val:
                actual_val = actual_val.replace('M', '')
                actual_val = float(actual_val) * 10**6
            elif 'B' in actual_val:
                actual_val = actual_val.replace('B', '')
                actual_val = float(actual_val) * 10**9
            elif 'T' in actual_val:
                actual_val = actual_val.replace('T', '')
                actual_val = float(actual_val) * 10**12
            elif '%' in actual_val:
                actual_val = actual_val.replace('%', '')
                actual_val = actual_val.replace('<', '')
                actual_val = float(actual_val) / 100
            elif '|' in actual_val:
                # TODO not sure if mean is the best approach here
                actual_vals = actual_val.split('|')
                actual_val = (float(actual_vals[0]) + float(actual_vals[1])) / 2
            else:
                actual_val = float(actual_val)

            return actual_val

        def update_scale_map(row):
            if row['title'] in self.scale_map.keys():
                self.scale_map[row['title']].append(row['actual'])
            else:
                self.scale_map[row['title']] = []

        def reduce_to_min_and_max(actual_values):
            _min = min(actual_values[1])
            _max = max(actual_values[1])
            if _min == _max:
                _min -= 1
                _max += 1

            return actual_values[0], [_min, _max]

        def scale_values(row):
            scaled = row['actual'] - self.scale_map[row['title']][0]
            scaled /= self.scale_map[row['title']][1] - self.scale_map[row['title']][0]

            if scaled > 1:
                # TODO check why in two cases row['actual'] is larger than previously counted max
                scaled = 1

            row['actual'] = scaled

            return row

        prices = pd.read_csv(self.res_dir + 'EURUSD.txt', sep=',', dtype=str, usecols=('<DTYYYYMMDD>','<TIME>','<HIGH>','<LOW>'))
        prices.index = pd.to_datetime(prices.pop('<DTYYYYMMDD>') + prices.pop('<TIME>'), format='%Y%m%d%H%M%S')
        prices['mean'] = (pd.to_numeric(prices.pop('<HIGH>')) + pd.to_numeric(prices.pop('<LOW>'))) / 2

        news = pd.read_csv(self.res_dir + 'forex-news.csv', sep=';', dtype=str, usecols=('date','time','symbol','title','actual'))
        news = news.loc[news['symbol'].isin(['EUR','USD']) & news['time'].str.contains('^\d{2}:')]
        news = news.loc[~news['actual'].isnull()]

        news_title_counts = dict(Counter(news['title'].tolist()))

        for k, v in news_title_counts.items():
            # if v >= 100:
            self.news_titles.append(k)

        self.news_symbols = list(set(news['symbol'].tolist()))

        news.index = pd.to_datetime(news.pop('date') + news.pop('time'), format='%Y-%m-%d%H:%M')
        news = news.loc[news.index >= prices.index[0]]

        news = news.apply(normalize_news_row, axis=1)
        # news = list(filter(lambda n: n is not None, news))

        news = news.loc[~news['actual'].isnull()]

        self.scale_map = dict(map(reduce_to_min_and_max, self.scale_map.items()))

        news = news.apply(scale_values, axis=1)

        labels = []

        # for k,v in prices.items():
        #     print(k)
            # quit()

        labels = []

        # news len = 11750
        # y len = 10181

        for news_datetime, n in news[::-1].iterrows():
            #TODO might check also larger intervals
            datetime_plus_interval = news_datetime + timedelta(hours=12)

            i = 0

            while True:
                prices_affected_by_news = prices.loc[(prices.index >= news_datetime) & (prices.index <= datetime_plus_interval)]
                if i > 10:
                    break
                elif len(prices_affected_by_news) < 100:
                    datetime_plus_interval += timedelta(hours=12)
                    i += 1
                else:
                    break

            if i > 10:
                print('last date: ', news_datetime)
                break

            price_when_news_happens = prices_affected_by_news.loc[prices_affected_by_news.index[0]]['mean']

            # TODO mean might not be the best approach. Try also e.g. highest value
            price_mean_in_affected_period = prices_affected_by_news['mean'].mean()

            diff = abs(price_mean_in_affected_period - price_when_news_happens)

            # TODO check percent ?
            # diff_threshold = 1
            label = 0
            if diff > 0.01:
                label = 1

            labels.append(label)

        #TODO parametrize interval
        #TODO separate to train_x, train_y, test_x, test_y

        x = news.as_matrix()[:len(labels)]
        y = labels

        if len(x) != len(y):
            raise RuntimeError('len(x): ' + str(len(x)) + ' does not equal len(y): ' + str(len(y)))

        length = len(x)
        breakpoint = int(round(length / 2))

        x_train = x[:-breakpoint]
        y_train = y[:-breakpoint]
        x_test = x[-breakpoint:]
        y_test = y[-breakpoint:]

        return x_train, y_train, x_test, y_test

analyzer = ForexAnalyzer()
