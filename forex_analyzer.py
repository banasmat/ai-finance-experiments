import pickle

import numpy as np

# from app.tensorflow.NeuralNetwork import NeuralNetwork
from app.dataset.DataSetProvider import DataSetProvider

data_set_provider = DataSetProvider()
# neural_network = NeuralNetwork()

#TODO
# we have to prepare system for creating 1 element datasets for predictions
# we have to save all symbols, symbol pairs, news titles, etc.
# (what if new title appears?) ideally: save for later retraining
# we can scrape news from website to csv
# but how do we get fresh prices?

# if Path('output/x_train_all.npy').is_file():

# x_train_all = np.load('output/x_train_all.npy')
# y_train_all = np.load('output/y_train_all.npy')
# x_test_all = np.load('output/x_test_all.npy')
# y_test_all = np.load('output/y_test_all.npy')
# else:
if __name__ == '__main__':
    x_train_all, y_train_all, x_test_all, y_test_all = data_set_provider.prepare_full_data_set()
    print(x_train_all)
# np.save('output/x_train_all.npy', x_train_all)
# np.save('output/y_train_all.npy', y_train_all)
# np.save('output/x_test_all.npy', x_test_all)
# np.save('output/y_test_all.npy', y_test_all)
#
# data = x_train_all, y_train_all, x_test_all, y_test_all
#
# with open('output/floydhub/data.pickle', 'wb') as f:
#     pickle.dump(data, f)

# neural_network.train(x_train_all, y_train_all, x_test_all, y_test_all)
