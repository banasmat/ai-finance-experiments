from DataProvider import DataProvider
from DataVisualizer import DataVisualizer

data_provider = DataProvider()
data_visualizer = DataVisualizer()

x_train, y_train, x_test, y_test = data_provider.get_data(False)

# TODO data_visualizer will need price data + labels(y)

print(x_train, y_train, x_test, y_test)