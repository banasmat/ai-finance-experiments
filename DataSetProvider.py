import numpy as np
import pandas as pd
from typing import List, Tuple

from PreProcessedDataProvider import PreProcessedDataProvider
from FeatureProvider import FeatureProvider
from LabelsProvider import LabelsProvider
from DataVisualizer import DataVisualizer


class DataSetProvider(object):

    prep_data_provider = PreProcessedDataProvider()
    feature_provider = FeatureProvider()
    labels_provider = LabelsProvider()
    data_visualizer = DataVisualizer()

    def prepare_data_set(self):
        symbol_pair_strings = self.prep_data_provider.get_symbol_pair_strings()
        symbol_pairs = self.prep_data_provider.get_symbol_pairs()
        all_symbols = list(set(symbol_pairs.flatten().tolist()))

        x_train_all = []
        y_train_all = []
        x_test_all = []
        y_test_all = []

        price_news_map = {}

        symbol_pairs = symbol_pairs[3:4]

        for symbol_pair in symbol_pairs:

            print('first run', symbol_pair)

            symbol_pair_str = symbol_pair[0] + symbol_pair[1]

            if symbol_pair_str not in price_news_map.keys():
                price_news_map[symbol_pair_str] = {}

            price_news_map[symbol_pair_str]['prices'] = self.prep_data_provider.get_price_data(symbol_pair[0],
                                                                                          symbol_pair[1])
            price_news_map[symbol_pair_str]['news'] = self.prep_data_provider.get_news_data(
                price_news_map[symbol_pair_str]['prices'].index[0], symbol_pair[0], symbol_pair[1])

        for symbol_pair in symbol_pairs:

            symbol_pair_str = symbol_pair[0] + symbol_pair[1]

            prices = price_news_map[symbol_pair_str]['prices']
            news = price_news_map[symbol_pair_str]['news']
            news = self.prep_data_provider.scale_news_data(news)
            news = self.feature_provider.add_preceding_price_feature(prices, news, symbol_pair[0] + symbol_pair[1],
                                                                refresh=True)

            # TODO features:
            # - rolling mean instead of price mean(?)
            # - volume (we don't have the data)
            # - rolling mean in last 24, 12, 6, now ?
            # OR recurrent neural network
            # + news as additional feature

            labels = self.labels_provider.get_labels(prices, news, symbol_pair[0] + symbol_pair[1], refresh=True)

            # self.data_visualizer.visualize(prices, news, labels)

            x_train, y_train, x_test, y_test = self.__get_data_set(news, labels,
                                                                   self.prep_data_provider.get_all_titles(),
                                                                   all_symbols, symbol_pair_strings)

            if len(x_train_all) is 0:
                x_train_all = x_train
                y_train_all = y_train
                x_test_all = x_test
                y_test_all = y_test
            else:

                print('1 shape x', x_train_all.shape)
                print('2 shape x', x_train.shape)

                print('1 shape y', y_train_all.shape)
                print('2 shape y', y_train.shape)

                x_train_all = np.append(x_train_all, x_train, axis=0)
                y_train_all = np.append(y_train_all, y_train, axis=0)
                x_test_all = np.append(x_test_all, x_test, axis=0)
                y_test_all = np.append(y_test_all, y_test, axis=0)

            print(len(x_train_all))
        return x_train_all, y_train_all, x_test_all, y_test_all

    def __get_data_set(self, news: pd.DataFrame, labels: np.ndarray, all_titles: List, all_currencies: List, all_pairs: List) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:

        all_labels = LabelsProvider.get_all_labels()

        news = self.__one_hot_from_all_items(news, 'preceding_price', all_labels)
        news = self.__one_hot_from_all_items(news, 'symbol', all_currencies)
        news = self.__one_hot_from_all_items(news, 'symbol_pair', all_pairs)
        news = self.__one_hot_from_all_items(news, 'title', all_titles)

        news = news.drop('datetime', 1)
        x = news.as_matrix()[:len(labels)]

        labels = self.__one_hot_from_all_items(pd.DataFrame(labels), 0, all_labels)

        y = labels.as_matrix()

        msk = np.random.rand(len(y)) < 0.8

        x_tra = x[msk]
        y_tra = y[msk]
        x_tes = x[~msk]
        y_tes = y[~msk]

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
