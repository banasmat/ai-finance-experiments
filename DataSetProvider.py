import numpy as np
import pandas as pd


class DataSetProvider(object):

    def get_dataset(self, news, labels):

        news = self.__convert_to_one_hot(news, 'symbol')
        # TODO consider normalizing titles: treating simmilar as one
        news = self.__convert_to_one_hot(news, 'title')

        news = news.drop('datetime', 1)
        x = news.as_matrix()[:len(labels)]

        labels = self.__convert_to_one_hot(pd.DataFrame(labels), 0)

        y = labels.as_matrix()
        # y = np.array(labels)

        msk = np.random.rand(len(y)) < 0.8

        x_tra = x[msk]
        y_tra = y[msk]
        x_tes = x[~msk]
        y_tes = y[~msk]

        return x_tra, y_tra, x_tes, y_tes

    @staticmethod
    def __convert_to_one_hot(df, col_name):
        one_hot = pd.get_dummies(df[col_name])
        df = df.drop(col_name, axis=1)
        df = df.join(one_hot)
        return df
