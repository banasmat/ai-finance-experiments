import pickle

import numpy as np

# from app.tensorflow.NeuralNetwork import NeuralNetwork
from app.dataset.DataSetProvider import DataSetProvider

data_set_provider = DataSetProvider()
# neural_network = NeuralNetwork()

#TODO nn should be retrained every month including new data

# if Path('output/x_train_all.npy').is_file():

# x_train_all = np.load('output/x_train_all.npy')
# y_train_all = np.load('output/y_train_all.npy')
# x_test_all = np.load('output/x_test_all.npy')
# y_test_all = np.load('output/y_test_all.npy')
# else:
if __name__ == '__main__':
    x_train_all, y_train_all, x_test_all, y_test_all = data_set_provider.prepare_full_data_set()
    print(x_train_all)

    np.save('output/x_train_all.npy', x_train_all)
    np.save('output/y_train_all.npy', y_train_all)
    np.save('output/x_test_all.npy', x_test_all)
    np.save('output/y_test_all.npy', y_test_all)

    data = x_train_all, y_train_all, x_test_all, y_test_all

    with open('output/floydhub/data.pickle', 'wb') as f:
        pickle.dump(data, f)

# neural_network.train(x_train_all, y_train_all, x_test_all, y_test_all)
