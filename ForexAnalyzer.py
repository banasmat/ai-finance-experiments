import numpy as np

from DataProvider import DataProvider

data_provider = DataProvider()

x_train, y_train, x_test, y_test = data_provider.get_data()

print(x_train, y_train, x_test, y_test)