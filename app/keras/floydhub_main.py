from KerasNeuralNetwork import KerasNeuralNetwork
import pickle
import numpy as np

with open('/dataset/data.pickle', 'rb') as f:
    x_train, y_train, x_test, y_test = pickle.load(f)

x_train = np.nan_to_num(x_train.round(8))
x_test = np.nan_to_num(x_test.round(8))

nn = KerasNeuralNetwork()

if __name__ == "__main__":
    nn.train(x_train, y_train.astype(float), x_test.round(0), y_test.astype(float))
    # print(nn.predict(x_test[0]))