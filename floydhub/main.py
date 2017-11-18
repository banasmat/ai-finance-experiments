from KerasNeuralNetwork import KerasNeuralNetwork
import pickle

# /dataset/data.pickle

with open('../output/data.pickle', 'rb') as f:
    x_train_all, y_train_all, x_test_all, y_test_all = pickle.load(f)

KerasNeuralNetwork.train(x_train_all, y_train_all, x_test_all, y_test_all)