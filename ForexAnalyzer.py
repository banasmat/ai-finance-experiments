from DataSetProvider import DataSetProvider
from DataVisualizer import DataVisualizer

data_set_provider = DataSetProvider()
data_visualizer = DataVisualizer()

x_train, y_train, x_test, y_test = data_set_provider.get_data(False)

data_visualizer.plot(y_train, y_test)