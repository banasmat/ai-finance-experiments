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
        labels = pd.DataFrame(list(map(lambda label: label is not 0, labels)))
        labels.index = news['datetime']

        prices = prices['mean'].resample('1H').mean()

        price_xs = prices.index.tolist()
        price_ys = prices.values.tolist()

        price_xs = list(map(self.__timestamp_to_datetime_string, price_xs))

        news_xs = []
        news_ys = []

        for label_datetime, label in labels.iterrows():
            news_xs.append(self.__timestamp_to_datetime_string(label_datetime))
            news_ys.append(prices.loc[label_datetime.round('h')])


        plt.plot(price_xs[:1000], price_ys[:1000], color='blue')
        plt.scatter(news_xs[:100], news_ys[:100], color='green')

        plt.xlim(price_xs[0], price_xs[100])
        plt.setp(plt.gca().xaxis.get_majorticklabels(),
                 'rotation', 90)

        # TODO scroll graph (use plotly ? )

        plt.show()

        return

    @staticmethod
    def __timestamp_to_datetime_string(timestamp):
        return timestamp.strftime('%Y-%m-%d %H')