from keras.models import Sequential
from keras.layers import Dense, SimpleRNN, Dropout
from keras.regularizers import L1L2
import numpy as np
import os


class XbrlRnn(object):

    def predict(self, x_test: np.array):

        regressor = self.create_model(x_test)
        regressor.load_weights(self.__get_model_path())

        return regressor.predict(x_test)

    def train(self, x_train, y_train):
        regressor = self.create_model(x_train)
        regressor.fit(x_train, y_train, epochs=200, batch_size=x_train.shape[0])

        regressor.save(self.__get_model_path())

    def create_model(self, x_data):
        regressor = Sequential()

        regressor.add(SimpleRNN(units=200, return_sequences=True, input_shape=(x_data.shape[1], x_data.shape[2])))
                # , kernel_regularizer=L1L2(0.01), activity_regularizer=L1L2(0.01), recurrent_regularizer=L1L2(0.01)))
        regressor.add(Dropout(0.2))

        regressor.add(SimpleRNN(units=200, return_sequences=True, activation='relu'))
        regressor.add(Dropout(0.2))

        regressor.add(SimpleRNN(units=200, return_sequences=True, activation='relu'))
        regressor.add(Dropout(0.2))

        regressor.add(SimpleRNN(units=100, activation='sigmoid'))
        regressor.add(Dropout(0.2))

        regressor.add(Dense(units=x_data.shape[1]))

        # RMSprop optimizer is usually used for rnn
        regressor.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        return regressor

    def __get_model_path(self):
        return os.path.join(os.path.abspath(os.getcwd()), 'app', 'xbrl', 'xbrl_rnn_model.h5')