import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from PreProcessedDataProvider import PreProcessedDataProvider
import pandas as pd


class DataVisualizer(object):

    prep_data_provider = PreProcessedDataProvider()

    def visualize(self, labels):

        prices = self.prep_data_provider.get_price_data()
        news = self.prep_data_provider.get_news_data(prices.index[0])

        x = news.as_matrix()[:len(labels)]
        y = np.array(labels)

        print('labels: ', len(labels))
        print('news: ', len(news))

        # TODO insert labels on price plot

        # plt.plot(prices)
        # plt.show()

        return
