import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from app.dataset.PreProcessedDataProvider import PreProcessedDataProvider


class RNNDatasetProvider(object):

    prep_data_provider = PreProcessedDataProvider()

    scaler_map = {}

    def prepare_dataset(self, prices: pd.DataFrame, main_col_name='close', lstm_length=120, gran='1H') -> (np.array, np.array):

        price_dataset: pd.DataFrame = prices.copy()

        for col in price_dataset.columns:

            if col not in self.scaler_map:
                self.scaler_map[col] = MinMaxScaler(feature_range=(0, 1))
            price_dataset[col] = self.scaler_map[col].fit_transform(price_dataset.loc[:, col].values.reshape(-1, 1))

        # Moving main column to front
        cols_order = price_dataset.columns.tolist()
        cols_order.insert(0, cols_order.pop(cols_order.index(main_col_name)))
        price_dataset = price_dataset[cols_order]

        xs = np.empty((price_dataset.shape[0], lstm_length, len(price_dataset.columns)))
        ys = np.empty((price_dataset.shape[0], 1))

        for i in range(lstm_length, len(price_dataset)):
            xs[i] = price_dataset.iloc[i - lstm_length:i].as_matrix()
            ys[i] = price_dataset[main_col_name][i]

        return xs, ys

    def add_news_to_dataset(self, prices, date_from, curr_1='EUR', curr_2='USD'):
        news = self.prep_data_provider.get_news_data(date_from, curr_1, curr_2)
        news = self.prep_data_provider.scale_news_data(news)

        #TODO consider adding title to dataset
        all_titles = self.prep_data_provider.get_all_titles()
        news.index = news['datetime'].dt.round('h')
        news: pd.DataFrame = news.drop(['symbol', 'symbol_pair', 'title'], axis=1)
        # news = data_set_provider.one_hot_from_all_items(news, 'title', all_titles)

        prices.loc[:, 'actual'] = 0
        prices.loc[:, 'forecast'] = 0
        prices.loc[:, 'previous'] = 0

        for dt, price in prices.iterrows():
            news_during_dt = news.loc[news.index == dt]
            if len(news_during_dt) > 0:
                prices.loc[dt, 'actual'] = news_during_dt['actual'].mean()
                prices.loc[dt, 'forecast'] = news_during_dt['forecast'].dropna().mean()
                prices.loc[dt, 'previous'] = news_during_dt['previous'].dropna().mean()

        prices.fillna(0, inplace=True)

        return prices

    def unscale_predictions(self, predictions, main_col_name='close'):
        return self.scaler_map[main_col_name].inverse_transform(predictions)
