import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM, TimeDistributed, Dropout, Activation
from keras.optimizers import SGD, Adadelta, Adam


class KerasNeuralNetwork:

    @staticmethod
    def train(x_train: np.ndarray, y_train: np.ndarray, x_test: np.ndarray, y_test: np.ndarray):

        batch_size = 32
        epochs = 100

        x_input_len = x_train.shape[1]
        y_input_len = y_train.shape[1]

        model = Sequential()

        model.add(Dense(512, input_shape=(x_input_len,)))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))

        model.add(Dense(512, input_shape=(x_input_len,)))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))

        model.add(Dense(y_input_len))
        model.add(Activation('softmax'))

        model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])

        history = model.fit(x_train, y_train,
                            batch_size=batch_size,
                            epochs=epochs,
                            verbose=1,
                            validation_split=0.1)

        print(model.summary())

        # model.fit(x_train, y_train, epochs=5, batch_size=64)

        loss_and_metrics = model.evaluate(x_test, y_test, batch_size=128)

        model.save('forex_analyzer_model.h5')

        print('accuracy', loss_and_metrics[1])
