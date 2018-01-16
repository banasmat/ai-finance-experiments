import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import os


class RNNDatasetProvider(object):

    def prepare_dataset(self, training_set, batch_size=60):

        sc = MinMaxScaler(feature_range=(0, 1))
        training_set_scaled = sc.fit_transform(training_set)

        x_train = []
        y_train = []

        for i in range(batch_size, len(training_set)):
            x_train.append(training_set_scaled[i - batch_size:i, 0])
            y_train.append(training_set_scaled[i, 0])
        x_train, y_train = np.array(x_train), np.array(y_train)

        num_of_helper_indicators = 1
        return np.reshape(x_train, (x_train.shape[0], x_train.shape[1], num_of_helper_indicators))
