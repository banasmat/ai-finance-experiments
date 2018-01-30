import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from app.dataset.PreProcessedDataProvider import PreProcessedDataProvider
from stockstats import StockDataFrame


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

        pd.options.mode.chained_assignment = None

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

    def add_rsi_to_dataset(self, prices, window_length=14):

        # Get the difference in price from previous step
        delta = prices['close'].diff()
        # Get rid of the first row, which is NaN since it did not have a previous
        # row to calculate the differences
        delta = delta[1:]

        # Make the positive gains (up) and negative gains (down) Series
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        # Calculate the EWMA
        # roll_up1 = pd.stats.moments.ewma(up, window_length)
        # roll_down1 = pd.stats.moments.ewma(down.abs(), window_length)
        #
        # # Calculate the RSI based on EWMA
        # rs_1 = roll_up1 / roll_down1
        # rsi_1 = 100.0 - (100.0 / (1.0 + rs_1))

        # Calculate the SMA
        roll_up2 = up.rolling(window_length).mean()
        roll_down2 = down.abs().rolling(window_length).mean()

        # Calculate the RSI based on SMA
        rs_2 = roll_up2 / roll_down2
        rsi_2 = 100.0 - (100.0 / (1.0 + rs_2))

        prices['rsi'] = round(rsi_2, 6)
        prices['rsi'] = np.nan_to_num(prices['rsi'])

        return prices

    def unscale_predictions(self, predictions, main_col_name='close'):
        return self.scaler_map[main_col_name].inverse_transform(predictions)
