from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import os


class XbrlRnn(object):

#TODO
# nie puszczać cików razem tylk osobno
# https://datascience.stackexchange.com/questions/27563/multi-dimentional-and-multivariate-time-series-forecast-rnn-lstm-keras

    def predict(self, x_test: np.array, gran='H1'):

        regressor = self.create_model(x_test)
        regressor.load_weights(self.__get_model_path(gran))

        return regressor.predict(x_test)

    def train(self, x_train, y_train, gran='H1'):
        regressor = self.create_model(x_train)
        regressor.fit(x_train, y_train, epochs=10, batch_size=32)
        regressor.save(self.__get_model_path(gran))

    def create_model(self, x_data):
        regressor = Sequential()

        regressor.add(LSTM(units=100, return_sequences=True, input_shape=(x_data.shape[1], x_data.shape[2])))
        regressor.add(Dropout(0.2))

        regressor.add(LSTM(units=100, return_sequences=True))
        regressor.add(Dropout(0.2))

        regressor.add(LSTM(units=100, return_sequences=True))
        regressor.add(Dropout(0.2))

        regressor.add(LSTM(units=50))
        regressor.add(Dropout(0.2))

        regressor.add(Dense(units=x_data.shape[1]))

        # RMSprop optimizer is usually used for rnn
        regressor.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

        return regressor

    def __get_model_path(self):
        return os.path.join(os.path.abspath(os.getcwd()), 'app', 'xbrl', 'xbrl_rnn_model.h5')