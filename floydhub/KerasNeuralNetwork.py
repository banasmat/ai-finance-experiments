import numpy as np
from keras.models import Sequential
from keras.layers import Dense


class KerasNeuralNetwork:

    @staticmethod
    def train(x_train: np.ndarray, y_train: np.ndarray, x_test: np.ndarray, y_test: np.ndarray):
        model = Sequential()

        model.add(Dense(units=64, activation='relu', input_dim=100))
        model.add(Dense(units=10, activation='softmax'))

        model.compile(loss='categorical_crossentropy',
                      optimizer='sgd',
                      metrics=['accuracy'])

        model.fit(x_train, y_train, epochs=5, batch_size=32)

        loss_and_metrics = model.evaluate(x_test, y_test, batch_size=128)

        model.save('forex_analyzer_model.h5')

        print(loss_and_metrics)
