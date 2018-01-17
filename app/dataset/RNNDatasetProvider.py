import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import os


class RNNDatasetProvider(object):

    def prepare_dataset(self, training_set: pd.DataFrame, batch_size=240):

        sc = MinMaxScaler(feature_range=(0, 1))

        for col in training_set.columns:
            training_set[col] = sc.fit_transform(training_set.loc[:, col].values.reshape(-1, 1))

        x_train = []
        y_train = []

        for i in range(batch_size, len(training_set)):
            x_train.append(training_set['close'][i - batch_size:i])
            y_train.append(training_set['close'][i])

        return np.array(x_train), np.array(y_train)