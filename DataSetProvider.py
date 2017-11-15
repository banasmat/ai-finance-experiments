import numpy as np
import pandas as pd
from typing import List, Tuple
from LabelsProvider import LabelsProvider


class DataSetProvider(object):
    def get_dataset(self, news: pd.DataFrame, labels: np.ndarray, all_titles: List, all_currencies: List, all_pairs: List) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:

        all_labels = LabelsProvider.get_all_labels()

        news = self.__one_hot_from_all_items(news, 'preceding_price', all_labels)
        news = self.__one_hot_from_all_items(news, 'symbol', all_currencies)
        news = self.__one_hot_from_all_items(news, 'symbol_pair', all_pairs)
        news = self.__one_hot_from_all_items(news, 'title', all_titles)

        news = news.drop('datetime', 1)
        x = news.as_matrix()[:len(labels)]

        labels = self.__one_hot_from_all_items(pd.DataFrame(labels), 0, all_labels)

        y = labels.as_matrix()
        # y = np.array(labels)

        msk = np.random.rand(len(y)) < 0.8

        x_tra: np.ndarray = x[msk]
        y_tra: np.ndarray = y[msk]
        x_tes: np.ndarray = x[~msk]
        y_tes: np.ndarray = y[~msk]

        return x_tra, y_tra, x_tes, y_tes

    @staticmethod
    def __one_hot_from_all_items(df: pd.DataFrame, column, all_items):
        # TODO consider normalizing titles further: treating simmilar as one
        one_hot = np.zeros((len(df[column]), len(all_items)))

        one_hot = pd.DataFrame(one_hot, columns=all_items, dtype=np.int)

        i = 0
        for news_title in df[column]:
            title_index = all_items.index(news_title)
            one_hot.iloc[i, title_index] = 1
            i += 1

        df = df.drop(column, axis=1)
        df = df.join(one_hot)

        return df
