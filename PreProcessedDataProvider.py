import pandas as pd


class PreProcessedDataProvider(object):
    res_dir = 'resources/'
    scale_map = {}

    def get_price_data(self):
        prices = pd.read_csv(self.res_dir + 'EURUSD.txt', sep=',', dtype=str,
                             usecols=('<DTYYYYMMDD>', '<TIME>', '<HIGH>', '<LOW>'))
        prices.index = pd.to_datetime(prices.pop('<DTYYYYMMDD>') + prices.pop('<TIME>'), format='%Y%m%d%H%M%S')
        prices['mean'] = (pd.to_numeric(prices.pop('<HIGH>')) + pd.to_numeric(prices.pop('<LOW>'))) / 2
        return prices

    def get_news_data(self, from_datetime):
        news = pd.read_csv(self.res_dir + 'forex-news.csv', sep=';', dtype=str,
                           usecols=('date', 'time', 'symbol', 'title', 'actual', 'forecast', 'previous'))

        news = news.loc[news['symbol'].isin(['EUR', 'USD']) & news['time'].str.contains('^\d{2}:')]
        news = news.loc[~news['actual'].isnull()]

        news['datetime'] = pd.to_datetime(news.pop('date') + news.pop('time'), format='%Y-%m-%d%H:%M')

        news = news.loc[news['datetime'] >= from_datetime]

        for key in ['actual', 'forecast', 'previous']:
            news[key] = news[key].apply(self.__normalize_numeric_string_value)
            news.apply(lambda row: self.__update_scale_map(row, key), axis=1)

        news = news.loc[~news['actual'].isnull()]

        for key in ['actual', 'forecast', 'previous']:
            self.scale_map[key] = dict(map(self.__reduce_to_min_and_max, self.scale_map[key].items()))
            news = news.apply(lambda row: self.__scale_values(row, key), axis=1)

        # reversing order
        news = news.iloc[::-1]

        return news

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

    def __scale_values(self, row, key):
        scaled = row[key] - self.scale_map[key][row['title']][0]
        scaled /= self.scale_map[key][row['title']][1] - self.scale_map[key][row['title']][0]

        if scaled > 1:
            # TODO check why in two cases row['actual'] is larger than previously counted max
            scaled = 1

        row['actual'] = float("{0:.2f}".format(scaled * 100))

        return row
