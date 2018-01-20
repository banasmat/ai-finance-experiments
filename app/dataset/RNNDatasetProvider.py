import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


class RNNDatasetProvider(object):

    scaler_map = {}

    def prepare_dataset(self, training_set: pd.DataFrame, lstm_length=120):

        training_set.is_copy = False

        for col in training_set.columns:

            if col not in self.scaler_map:
                self.scaler_map[col] = MinMaxScaler(feature_range=(0, 1))
            training_set[col] = self.scaler_map[col].fit_transform(training_set.loc[:, col].values.reshape(-1, 1))

        # cols_order = ['close', 'open', 'high', 'low', 'volume']
        cols_order = ['close', 'volume']
        training_set = training_set[cols_order]

        x_train = np.empty((training_set.shape[0], lstm_length, len(training_set.columns)))
        y_train = np.empty((training_set.shape[0], 1))

        for i in range(lstm_length, len(training_set)):
            x_train[i] = training_set.iloc[i - lstm_length:i].as_matrix()
            y_train[i] = training_set['close'][i]

        return x_train, y_train
