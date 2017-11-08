import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go


class DataVisualizer(object):

    def visualize(self, prices, news, labels):

        news = news.iloc[:len(labels)]
        news_labels = pd.DataFrame(labels)
        news_labels.index = news['datetime']

        prices = prices['mean'].resample('1H').mean()

        price_xs = prices.index.tolist()
        price_ys = prices.values.tolist()

        price_xs = list(map(self.__timestamp_to_datetime_string, price_xs))

        news_up_xs, news_up_ys = self.__prepare_news_lists(prices, news_labels, 1)
        news_down_xs, news_down_ys = self.__prepare_news_lists(prices, news_labels, -1)

        trace0 = go.Scattergl(
            x=np.array(price_xs),
            y=np.array(price_ys),
            mode='lines',
            fillcolor='blue'
        )
        trace1 = go.Scattergl(
            x=np.array(news_up_xs),
            y=np.array(news_up_ys),
            mode='markers',
            fillcolor='green'
        )
        trace2 = go.Scattergl(
            x=np.array(news_down_xs),
            y=np.array(news_down_ys),
            mode='markers',
            fillcolor='red'
        )

        py.plot([trace0, trace1, trace2], filename='eurusd')

        return

    @staticmethod
    def __timestamp_to_datetime_string(timestamp):
        return timestamp.strftime('%Y-%m-%d %H')
    
    def __prepare_news_lists(self, prices, news_labels, label_val):
        news_labels = news_labels.loc[news_labels[0] == label_val]

        news_xs = []
        news_ys = []

        for label_datetime, label in news_labels.iterrows():
            news_xs.append(self.__timestamp_to_datetime_string(label_datetime))
            news_ys.append(prices.loc[label_datetime.round('h')])

        return news_xs, news_ys
