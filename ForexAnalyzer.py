from PreProcessedDataProvider import PreProcessedDataProvider
from LabelsProvider import LabelsProvider
from DataSetProvider import DataSetProvider
from DataVisualizer import DataVisualizer
from NeuralNetwork import NeuralNetwork

prep_data_provider = PreProcessedDataProvider()
labels_provider = LabelsProvider()
data_set_provider = DataSetProvider()
data_visualizer = DataVisualizer()
neural_network = NeuralNetwork()

prices = prep_data_provider.get_price_data()
news = prep_data_provider.get_news_data(prices.index[0])

labels = labels_provider.get_labels(prices, news, refresh=False)

# data_visualizer.visualize(prices, news, labels)

x_train, y_train, x_test, y_test = data_set_provider.get_dataset(news, labels)
neural_network.train(x_train, y_train, x_test, y_test)
