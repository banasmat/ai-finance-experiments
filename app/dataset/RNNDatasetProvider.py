import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


class RNNDatasetProvider(object):

    def prepare_dataset(self, training_set: pd.DataFrame, batch_size=240):

        sc = MinMaxScaler(feature_range=(0, 1))

        for col in training_set.columns:
            training_set[col] = sc.fit_transform(training_set.loc[:, col].values.reshape(-1, 1))

        cols_order = ['close', 'open', 'high', 'low', 'volume']
        training_set = training_set[cols_order]

        x_train = np.empty((training_set.shape[0], batch_size, len(training_set.columns)))
        y_train = np.empty((training_set.shape[0], 1))

        for i in range(batch_size, len(training_set)):
            x_train[i] = training_set.iloc[i - batch_size:i].as_matrix()
            y_train[i] = training_set['close'][i]

        return x_train, y_train
