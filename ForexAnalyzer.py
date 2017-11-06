from DataSetProvider import DataSetProvider
from DataVisualizer import DataVisualizer
import numpy as np

data_set_provider = DataSetProvider()
data_visualizer = DataVisualizer()

x_train, y_train, x_test, y_test = data_set_provider.get_data(True)

data_visualizer.visualize(np.append(y_train, y_test))