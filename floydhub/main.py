from KerasNeuralNetwork import KerasNeuralNetwork
import pickle
from keras.datasets import fashion_mnist
import numpy as np

(x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

# with open('/dataset/data.pickle', 'rb') as f:
with open('../output/data.pickle', 'rb') as f:
    x_train, y_train, x_test, y_test = pickle.load(f)

x_train = np.nan_to_num(x_train.round(4))
x_test = np.nan_to_num(x_test.round(4))

KerasNeuralNetwork.train(x_train, y_train.astype(float), x_test.round(0), y_test.astype(float))