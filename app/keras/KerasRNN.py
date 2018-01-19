from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import os


class KerasRNN(object):

    def predict(self, x_test: np.array):
        # inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
        # inputs = inputs.reshape(-1, 1)
        # inputs = sc.transform(inputs)
        #
        # x_test = []
        # for i in range(60, 80):
        #     x_test.append(inputs[i - 60:i, 0])
        # x_test = np.array(x_test)
        #
        # x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], num_of_helper_indicators))

        regressor = self.create_model(x_test)
        regressor.load_weights(os.path.join(os.path.abspath(os.getcwd()), 'app', 'keras', 'rnn_model.h5'))

        predicted_stock_price = regressor.predict(x_test)
        # predicted_stock_price = sc.inverse_transform(predicted_stock_price)

    def test(self, x_test, y_test):
        regressor = self.create_model(x_test)
        regressor.load_weights(os.path.join(os.path.abspath(os.getcwd()), 'app', 'keras', 'rnn_model.h5'))
        #TODO

    def train(self, x_train, y_train):
        regressor = self.create_model(x_train)
        regressor.fit(x_train, y_train, epochs=100, batch_size=32)
        regressor.save('rnn_model.h5')

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

