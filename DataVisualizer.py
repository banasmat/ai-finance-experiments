import matplotlib.pyplot as plt
from PreProcessedDataProvider import PreProcessedDataProvider
import pandas as pd


class DataVisualizer(object):

    prep_data_provider = PreProcessedDataProvider()

    def visualize(self, labels):

        plt.style.use('ggplot')

        prices = self.prep_data_provider.get_price_data()
        news = self.prep_data_provider.get_news_data(prices.index[0])

        news = news.iloc[:len(labels)]

        prices = prices['mean'].resample('1H').mean()

        price_xs = prices.index.tolist()
        price_ys = prices.values.tolist()

        price_xs = list(map(self.__timestamp_to_datetime_string, price_xs))

        news_up_xs, news_up_ys = self.__prepare_news_lists(prices, news, labels, 1)
        news_down_xs, news_down_ys = self.__prepare_news_lists(prices, news, labels, -1)

        plt.plot(price_xs[:1000], price_ys[:1000], color='blue')
        plt.scatter(news_up_xs[:100], news_up_ys[:100], color='green')
        plt.scatter(news_down_xs[:100], news_down_ys[:100], color='red')

        plt.xlim(price_xs[0], price_xs[100])
        plt.setp(plt.gca().xaxis.get_majorticklabels(),
                 'rotation', 90)

        # TODO scroll graph (use plotly ? )

        plt.show()

        return

    @staticmethod
    def __timestamp_to_datetime_string(timestamp):
        return timestamp.strftime('%Y-%m-%d %H')
    
    def __prepare_news_lists(self, prices, news, labels, label_val):
        news_labels = pd.DataFrame(list(map(lambda lab: lab == label_val, labels)))
        news_labels.index = news['datetime']
        news_xs = []
        news_ys = []

        for label_datetime, label in news_labels.iterrows():
            news_xs.append(self.__timestamp_to_datetime_string(label_datetime))
            news_ys.append(prices.loc[label_datetime.round('h')])

        return news_xs, news_ys
