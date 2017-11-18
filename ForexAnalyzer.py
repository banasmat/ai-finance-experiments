from DataSetProvider import DataSetProvider
from NeuralNetwork import NeuralNetwork
import numpy as np
import pickle
from pathlib import Path

data_set_provider = DataSetProvider()
neural_network = NeuralNetwork()


if Path('output/x_train_all.npy').is_file():
    x_train_all = np.load('output/x_train_all.npy')
    y_train_all = np.load('output/y_train_all.npy')
    x_test_all = np.load('output/x_test_all.npy')
    y_test_all = np.load('output/y_test_all.npy')
else:
    x_train_all, y_train_all, x_test_all, y_test_all = data_set_provider.prepare_data_set()

    np.save('output/x_train_all.npy', x_train_all)
    np.save('output/y_train_all.npy', y_train_all)
    np.save('output/x_test_all.npy', x_test_all)
    np.save('output/y_test_all.npy', y_test_all)

data = x_train_all, y_train_all, x_test_all, y_test_all

with open('output/data.pickle', 'wb') as f:
    pickle.dump(data, f)

# neural_network.train(x_train_all, y_train_all, x_test_all, y_test_all)
