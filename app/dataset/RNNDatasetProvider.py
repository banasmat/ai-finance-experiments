import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


class RNNDatasetProvider(object):

    scaler_map = {}

    def prepare_dataset(self, prices: pd.DataFrame, main_col_name='close', lstm_length=120) -> (np.array, np.array):

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

    def unscale_predictions(self, predictions, main_col_name='close'):
        return self.scaler_map[main_col_name].inverse_transform(predictions)
