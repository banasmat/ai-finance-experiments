from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import os


class KerasRNN(object):

    model_path = os.path.join(os.path.abspath(os.getcwd()), 'app', 'keras', 'rnn_model.h5')

    def predict(self, x_test: np.array):

        regressor = self.create_model(x_test)
        regressor.load_weights(self.model_path)

        return regressor.predict(x_test)

    def train(self, x_train, y_train):
        regressor = self.create_model(x_train)
        regressor.fit(x_train, y_train, epochs=60, batch_size=32)
        regressor.save(self.model_path)

    def create_model(self, x_data):
        regressor = Sequential()

        regressor.add(LSTM(units=50, return_sequences=True, input_shape=(x_data.shape[1], x_data.shape[2])))
        regressor.add(Dropout(0.2))

        regressor.add(LSTM(units=50, return_sequences=True))
        regressor.add(Dropout(0.2))

        regressor.add(LSTM(units=50, return_sequences=True))
        regressor.add(Dropout(0.2))

        regressor.add(LSTM(units=50))
        regressor.add(Dropout(0.2))

        regressor.add(Dense(units=1))

        # RMSprop optimizer is usually used for rnn
        regressor.compile(optimizer='adam', loss='mean_squared_error')

        return regressor

