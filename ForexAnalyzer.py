from PreProcessedDataProvider import PreProcessedDataProvider
from FeatureProvider import FeatureProvider
from LabelsProvider import LabelsProvider
from DataSetProvider import DataSetProvider
from DataVisualizer import DataVisualizer
# from NeuralNetwork import NeuralNetwork


prep_data_provider = PreProcessedDataProvider()
feature_provider = FeatureProvider()
labels_provider = LabelsProvider()
data_set_provider = DataSetProvider()
data_visualizer = DataVisualizer()
# neural_network = NeuralNetwork()

# TODO get prices separately for all symbols
# for every symbol get news with features
# for every symbol get labels
# glue labels into one array

value_pairs = prep_data_provider.get_price_value_pairs()

x_train_all, y_train_all, x_test_all, y_test_all = [], [], [], []

for value_pair in value_pairs:
    prices = prep_data_provider.get_price_data(value_pair[0], value_pair[1])
    news = prep_data_provider.get_news_data(prices.index[0], value_pair[0], value_pair[1])
    news = feature_provider.add_preceding_price_feature(prices, news, value_pair[0] + value_pair[1], refresh=False)

    labels = labels_provider.get_labels(prices, news, value_pair[0] + value_pair[1], refresh=False)

    # data_visualizer.visualize(prices, news, labels)

    x_train, y_train, x_test, y_test = data_set_provider.get_dataset(news, labels)

    x_train_all.append(x_train)
    y_train_all.append(y_train)
    x_test_all.append(x_test)
    y_test_all.append(y_test)

quit()



# neural_network.train(x_train_all, y_train_all, x_test_all, y_test_all)
