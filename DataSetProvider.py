import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from PreProcessedDataProvider import PreProcessedDataProvider

class DataSetProvider(object):

    prep_data_provider = PreProcessedDataProvider()

    def get_data(self, refresh=True):

        x_tra = np.load('output/x_train.npy')
        y_tra = np.load('output/y_train.npy')
        x_tes = np.load('output/x_test.npy')
        y_tes = np.load('output/y_test.npy')

        if refresh is False:
            return x_tra, y_tra, x_tes, y_tes

        prices = self.prep_data_provider.get_price_data()

        news = self.prep_data_provider.get_news_data(prices.index[0])

        news = self.__convert_to_one_hot(news, 'symbol')
        # TODO consider normalizing titles: treating simmilar as one
        news = self.__convert_to_one_hot(news, 'title')

        labels = []

        # FIXME more labels are outputted than news ...
        for news_datetime, n in news.iterrows():
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


    def __convert_to_one_hot(self, df, col_name):
        one_hot = pd.get_dummies(df[col_name])
        df = df.drop(col_name, axis=1)
        df = df.join(one_hot)
        return df