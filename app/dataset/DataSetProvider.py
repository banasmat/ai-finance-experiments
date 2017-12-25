from typing import List, Tuple

import numpy as np
import pandas as pd

from .DataVisualizer import DataVisualizer
from .FeatureProvider import FeatureProvider
from .LabelsProvider import LabelsProvider
from .PreProcessedDataProvider import PreProcessedDataProvider
from app.model.CalendarEntry import CalendarEntry
from app.model.PriceQuote import PriceQuote


class DataSetProvider(object):

    prep_data_provider = PreProcessedDataProvider()
    feature_provider = FeatureProvider()
    labels_provider = LabelsProvider()
    data_visualizer = DataVisualizer()

    def prepare_single_data_set(self, calendar_entry: CalendarEntry, price_quotes: List[PriceQuote], currency_pair: str):
        return self.__get_news_matrix(self.data_frames_from_records([calendar_entry], price_quotes, currency_pair)[1])

    def data_frames_from_records(self, calendar_entries: List[CalendarEntry], price_quotes: List[PriceQuote], currency_pair: str):
        self.prep_data_provider.load_scale_map()

        news_dicts = list(map(lambda entry: entry.to_dict(), calendar_entries))
        # news_dicts = list(map(lambda entry: entry.to_dict(), calendar_entries))

        news = pd.DataFrame.from_records(news_dicts)

        news['symbol_pair'] = currency_pair

        price_dicts = list(map(lambda quote: quote.to_dict(), price_quotes))

        prices = pd.DataFrame.from_records(price_dicts)
        prices.index = prices.pop('datetime')

        prices['mean'] = (prices.pop('high') + prices.pop('low')) / 2
        prices = prices['mean'].resample('1H').mean()

        for key in ['actual', 'forecast', 'previous']:
            news[key] = news[key].apply(self.prep_data_provider.normalize_numeric_string_value)

        news = self.prep_data_provider.scale_news_data(news)
        news = self.feature_provider.add_preceding_price_feature(prices, news)

        return prices, news

    def prepare_full_data_set(self):
        currency_pairs = self.prep_data_provider.get_currency_pairs()

        x_train_all = []
        y_train_all = []
        x_test_all = []
        y_test_all = []

        price_news_map = {}

        # symbol_pairs = symbol_pairs[3:5]

        for currency_pair in currency_pairs:

            print('first run', currency_pair)

            symbol_pair_str = currency_pair[0] + currency_pair[1]

            if symbol_pair_str not in price_news_map.keys():
                price_news_map[symbol_pair_str] = {}

            price_news_map[symbol_pair_str]['prices'] = self.prep_data_provider.get_price_data(currency_pair[0],
                                                                                          currency_pair[1])
            price_news_map[symbol_pair_str]['news'] = self.prep_data_provider.get_news_data(
                price_news_map[symbol_pair_str]['prices'].index[0], currency_pair[0], currency_pair[1])

        for currency_pair in currency_pairs:

            symbol_pair_str = currency_pair[0] + currency_pair[1]

            prices = price_news_map[symbol_pair_str]['prices']
            news = price_news_map[symbol_pair_str]['news']
            news = self.prep_data_provider.scale_news_data(news)
            news = self.feature_provider.add_preceding_price_feature(prices, news)

            # TODO features:
            # - rolling mean instead of price mean(?)
            # - volume (we don't have the data)
            # - rolling mean in last 24, 12, 6, now ?
            # OR recurrent neural network
            # + news as additional feature

            labels = self.labels_provider.get_labels(prices, news)

            # self.data_visualizer.visualize(prices, news, labels)

            x_train, y_train, x_test, y_test = self.__get_full_data_set(news, labels)

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

        self.prep_data_provider.save_scale_map()

        return x_train_all, y_train_all, x_test_all, y_test_all

    def __get_full_data_set(self, news: pd.DataFrame, labels: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:

        x = self.__get_news_matrix(news, len(labels))

        # all_labels = LabelsProvider.get_all_labels()
        # labels = self.__one_hot_from_all_items(pd.DataFrame(labels), 0, all_labels)
        # y = labels.as_matrix()
        y = labels

        msk = np.random.rand(len(y)) < 0.8

        x_tra = x[msk]
        y_tra = y[msk]
        x_tes = x[~msk]
        y_tes = y[~msk]

        return x_tra, y_tra, x_tes, y_tes

    def __get_news_matrix(self, news: pd.DataFrame, max_len=1):

        all_titles = self.prep_data_provider.get_all_titles()
        all_pairs = self.prep_data_provider.get_currency_pair_strings()
        all_currencies = self.prep_data_provider.get_all_currencies()

        news = news.reset_index(drop=True)

        # news = self.__one_hot_from_all_items(news, 'preceding_price', all_labels)
        news['preceding_price'].apply(lambda x: x * 10)
        news = self.__one_hot_from_all_items(news, 'symbol', all_currencies)
        news = self.__one_hot_from_all_items(news, 'symbol_pair', all_pairs)
        news = self.__one_hot_from_all_items(news, 'title', all_titles)

        news = news.drop('datetime', 1)
        return news.as_matrix()[:max_len]


    @staticmethod
    def __one_hot_from_all_items(df: pd.DataFrame, column, all_items) -> pd.DataFrame:
        # TODO consider normalizing titles further: treating simmilar as one
        one_hot = np.zeros((len(df[column]), len(all_items)), dtype=np.int)

        one_hot = pd.DataFrame(one_hot, columns=all_items, dtype=np.int)

        i = 0
        for news_title in df[column]:
            title_index = all_items.index(news_title)
            one_hot.iloc[i, title_index] = 1
            i += 1

        one_hot = one_hot.drop(one_hot.columns[0], axis=1)

        df = df.drop(column, axis=1)
        df = df.join(one_hot)

        return df
