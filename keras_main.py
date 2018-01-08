from app.keras.KerasNeuralNetwork import KerasNeuralNetwork
import pickle
import numpy as np
import os

with open(os.path.join(os.path.abspath(os.getcwd()), 'output', 'floydhub', 'data.pickle'), 'rb') as f:
    x_train, y_train, x_test, y_test = pickle.load(f)

x_train = np.nan_to_num(x_train.round(8)).astype(float)
x_test = np.nan_to_num(x_test.round(8)).astype(float)

x_test = x_test.round(0)

nn = KerasNeuralNetwork()

if __name__ == "__main__":
    nn.train(x_train, y_train, x_test, y_test)
    print('\naccuracy', nn.test(x_test, y_test))
