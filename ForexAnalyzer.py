from PreProcessedDataProvider import PreProcessedDataProvider
from FeatureProvider import FeatureProvider
from LabelsProvider import LabelsProvider
from DataSetProvider import DataSetProvider
from DataVisualizer import DataVisualizer
from NeuralNetwork import NeuralNetwork
import numpy as np

prep_data_provider = PreProcessedDataProvider()
feature_provider = FeatureProvider()
labels_provider = LabelsProvider()
data_set_provider = DataSetProvider()
data_visualizer = DataVisualizer()
neural_network = NeuralNetwork()

currency_pairs = prep_data_provider.get_currency_pairs()
all_currencies = list(set(currency_pairs.flatten().tolist()))

x_train_all = []
y_train_all = []
x_test_all = []
y_test_all = []

price_news_map = {}

for currency_pair in currency_pairs:

    currency_pair_str = currency_pair[0] + currency_pair[1]

    if currency_pair_str not in price_news_map.keys():
        price_news_map[currency_pair_str] = {}

    price_news_map[currency_pair_str]['prices'] = prep_data_provider.get_price_data(currency_pair[0], currency_pair[1])
    price_news_map[currency_pair_str]['news'] = prep_data_provider.get_news_data(price_news_map[currency_pair_str]['prices'].index[0], currency_pair[0], currency_pair[1])

for currency_pair in currency_pairs:

    print(currency_pair)

    currency_pair_str = currency_pair[0] + currency_pair[1]

    prices = price_news_map[currency_pair_str]['prices']
    news = price_news_map[currency_pair_str]['news']
    news = prep_data_provider.scale_news_data(news)
    news = feature_provider.add_preceding_price_feature(prices, news, currency_pair[0] + currency_pair[1], refresh=True)

    labels = labels_provider.get_labels(prices, news, currency_pair[0] + currency_pair[1], refresh=True)

    # data_visualizer.visualize(prices, news, labels)

    x_train, y_train, x_test, y_test = data_set_provider.get_dataset(news, labels, prep_data_provider.get_all_titles(), all_currencies)

    if len(x_train_all) is 0:
        x_train_all = x_train
        y_train_all = y_train
        x_test_all = x_test
        y_test_all = y_test
    else:
        x_train_all = np.append(x_train_all, x_train, axis=0)
        y_train_all = np.append(y_train_all, y_train, axis=0)
        x_test_all = np.append(x_test_all, x_test, axis=0)
        y_test_all = np.append(y_test_all, y_test, axis=0)

np.save('output/x_train_all.npy', x_train_all)
np.save('output/y_train_all.npy', y_train_all)
np.save('output/x_test_all.npy', x_test_all)
np.save('output/y_test_all.npy', y_test_all)

neural_network.train(x_train_all, y_train_all, x_test_all, y_test_all)
