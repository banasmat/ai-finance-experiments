import pandas as pd

# TODO rename to PreProcessedDataProvider (?)
class PreProcessedDataProvider(object):

    res_dir = 'resources/'
    scale_map = {}

    def get_price_data(self):
        prices = pd.read_csv(self.res_dir + 'EURUSD.txt', sep=',', dtype=str, usecols=('<DTYYYYMMDD>','<TIME>','<HIGH>','<LOW>'))
        prices.index = pd.to_datetime(prices.pop('<DTYYYYMMDD>') + prices.pop('<TIME>'), format='%Y%m%d%H%M%S')
        prices['mean'] = (pd.to_numeric(prices.pop('<HIGH>')) + pd.to_numeric(prices.pop('<LOW>'))) / 2
        return prices

    def get_news_data(self, from_datetime):
        news = pd.read_csv(self.res_dir + 'forex-news.csv', sep=';', dtype=str, usecols=('date','time','symbol','title','actual'))

        news = news.loc[news['symbol'].isin(['EUR','USD']) & news['time'].str.contains('^\d{2}:')]
        news = news.loc[~news['actual'].isnull()]

        news.index = pd.to_datetime(news.pop('date') + news.pop('time'), format='%Y-%m-%d%H:%M')

        news = news.loc[news.index >= from_datetime]
        news = news.apply(self.__normalize_actual_value, axis=1)
        news = news.loc[~news['actual'].isnull()]

        self.scale_map = dict(map(self.__reduce_to_min_and_max, self.scale_map.items()))
        news = news.apply(self.__scale_values, axis=1)

        return news


    def __normalize_actual_value(self, row):

        actual_val = row['actual']

        try:

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

        except ValueError:
            return None

        row['actual'] = actual_val
        self.__update_scale_map(row)
        return row

    def __update_scale_map(self, row):
        if row['title'] in self.scale_map.keys():
            self.scale_map[row['title']].append(row['actual'])
        else:
            self.scale_map[row['title']] = []

    def __reduce_to_min_and_max(self, actual_values):
        _min = min(actual_values[1])
        _max = max(actual_values[1])
        if _min == _max:
            _min -= 1
            _max += 1

        return actual_values[0], [_min, _max]

    def __scale_values(self, row):
        scaled = row['actual'] - self.scale_map[row['title']][0]
        scaled /= self.scale_map[row['title']][1] - self.scale_map[row['title']][0]

        if scaled > 1:
            # TODO check why in two cases row['actual'] is larger than previously counted max
            scaled = 1

        row['actual'] = float("{0:.2f}".format(scaled * 100))

        return row
