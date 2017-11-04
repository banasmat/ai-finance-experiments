import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from PreProcessedDataProvider import PreProcessedDataProvider
import pandas as pd


class DataVisualizer(object):

    prep_data_provider = PreProcessedDataProvider()

    def plot(self, y_train,  y_test):

        prices = self.prep_data_provider.get_price_data()

        # FIXME we need labels(y) with dates

        plt.plot(prices)
        plt.show()

        return
