import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from PreProcessedDataProvider import PreProcessedDataProvider

class DataSetProvider(object):

    prep_data_provider = PreProcessedDataProvider()
    scale_map = {}

    def get_data(self, refresh=True):

        x_tra = np.load('output/x_train.npy')
        y_tra = np.load('output/y_train.npy')
        x_tes = np.load('output/x_test.npy')
        y_tes = np.load('output/y_test.npy')

        if refresh is False:
            return x_tra, y_tra, x_tes, y_tes

        prices = self.prep_data_provider.get_price_data()

        news = self.prep_data_provider.get_news_data()
        news = news.loc[news['symbol'].isin(['EUR','USD']) & news['time'].str.contains('^\d{2}:')]
        news = news.loc[~news['actual'].isnull()]

        news.index = pd.to_datetime(news.pop('date') + news.pop('time'), format='%Y-%m-%d%H:%M')
        news = news.loc[news.index >= prices.index[0]]

        news = news.apply(self.normalize_actual_value, axis=1)

        news = news.loc[~news['actual'].isnull()]
        self.scale_map = dict(map(self.__reduce_to_min_and_max, self.scale_map.items()))
        news = news.apply(self.__scale_values, axis=1)

        news = self.__convert_to_one_hot(news, 'symbol')
        # TODO consider normalizing titles: treating simmilar as one
        news = self.__convert_to_one_hot(news, 'title')

        labels = []

        j = 0
        for news_datetime, n in news.iterrows():
            #TODO might check also larger intervals
            datetime_plus_interval = news_datetime + timedelta(hours=12)

            j += 1
            i = 0

            while True:
                prices_affected_by_news = prices.loc[(prices.index >= news_datetime) & (prices.index <= datetime_plus_interval)]
                if i > 10:
                    break
                elif len(prices_affected_by_news) < 100:
                    # FIXME it seems to make a lot of news use the same price diffs as labels
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

            diff_percent = diff / price_when_news_happens * 100

            # print(diff_percent)

            # TODO check percent ?
            diff_threshold = 0.2
            label = 0
            if diff_percent > diff_threshold:
                label = 1

            labels.append(label)

        #TODO parametrize interval
        #TODO separate to train_x, train_y, test_x, test_y

        x = news.as_matrix()[:len(labels)]
        y = np.array(labels)

        if len(x) != len(y):
            raise RuntimeError('len(x): ' + str(len(x)) + ' does not equal len(y): ' + str(len(y)))

        msk = np.random.rand(len(y)) < 0.8

        x_tra = x[msk]
        y_tra = y[msk]
        x_tes = x[~msk]
        y_tes = y[~msk]

        np.save('output/x_train.npy', x_tra)
        np.save('output/y_train.npy', y_tra)
        np.save('output/x_test.npy', x_tes)
        np.save('output/y_test.npy', y_tes)

        np.savetxt('output/x_train.txt', x_tra)
        np.savetxt('output/y_train.txt', y_tra)
        np.savetxt('output/x_test.txt', x_tes)
        np.savetxt('output/y_test.txt', y_tes)

        return x_tra, y_tra, x_tes, y_tes


    def normalize_actual_value(self, row):

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

    def __convert_to_one_hot(self, df, col_name):
        one_hot = pd.get_dummies(df[col_name])
        df = df.drop(col_name, axis=1)
        df = df.join(one_hot)
        return df

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
