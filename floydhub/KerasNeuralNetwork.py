import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM, TimeDistributed, Dropout, Activation


class KerasNeuralNetwork:

    @staticmethod
    def train(x_train: np.ndarray, y_train: np.ndarray, x_test: np.ndarray, y_test: np.ndarray):

        x_input_len = x_train.shape[1]
        y_input_len = y_train.shape[1]

        x_y_input_len_avg = int((x_input_len + y_input_len)/2)

        model = Sequential()

        model.add(Dense(units=x_y_input_len_avg,
                        activation='relu',
                        kernel_initializer='uniform',
                        input_shape=(x_input_len,)
                        ))
        #TODO activate dropout in case of overfitting (big difference between training and testing accuracy)
        #model.add(Dropout(p=0.1))

        model.add(Dense(units=x_y_input_len_avg,
                        activation='relu',
                        kernel_initializer='uniform',
                        ))
        #model.add(Dropout(p=0.1))

        model.add(Dense(units=y_input_len,
                        activation='tahn',
                        kernel_initializer='uniform',
                        ))

        model.compile(loss='mean_squared_error',
                      optimizer='adam',
                      metrics=['accuracy'])

        model.fit(x_train, y_train,
                  batch_size=10,
                  epochs=10,
                  # verbose=1,
                  # validation_split=0.1
                  )

        print(model.summary())

        # model.fit(x_train, y_train, epochs=5, batch_size=64)

        loss_and_metrics = model.evaluate(x_test, y_test, batch_size=128)

        model.save('forex_analyzer_model.h5')

        print('accuracy', loss_and_metrics[1])
