from datetime import datetime

import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go


class DataVisualizer(object):

    def visualize(self, prices, news, labels):

        news = news.iloc[:len(labels)]
        news_labels = pd.DataFrame(labels)

        news_labels.index = news['datetime'].dt.round('h')

        prices = prices['mean'].resample('1H').mean()

        price_xs = prices.index.tolist()
        price_ys = prices.values.tolist()

        price_xs = list(map(self.__timestamp_to_datetime_string, price_xs))

        news_up_ys = self.__get_news_ys(prices, news_labels, 1)
        news_down_ys = self.__get_news_ys(prices, news_labels, -1)
        news_up_ys_lg = self.__get_news_ys(prices, news_labels, 2)
        news_down_ys_lg = self.__get_news_ys(prices, news_labels, -2)

        trace0 = go.Scattergl(
            x=np.array(price_xs),
            y=np.array(price_ys),
            mode='lines',
            fillcolor='blue',
            name='prices'
        )
        trace1 = go.Scattergl(
            x=np.array(price_xs),
            y=np.array(news_up_ys),
            mode='markers',
            marker=dict(
                color='rgb(0,255,0)',
                size=5
            ),
            name='news - buy signals'
        )
        trace2 = go.Scattergl(
            x=np.array(price_xs),
            y=np.array(news_down_ys),
            mode='markers',
            marker=dict(
                color='rgb(255,0,0)',
                size=5
            ),
            name='news - sell signals'
        )
        trace3 = go.Scattergl(
            x=np.array(price_xs),
            y=np.array(news_up_ys_lg),
            mode='markers',
            marker=dict(
                color='rgb(0,255,0)',
                size=10
            ),
            name='news - buy signals'
        )
        trace4 = go.Scattergl(
            x=np.array(price_xs),
            y=np.array(news_down_ys_lg),
            mode='markers',
            marker=dict(
                color='rgb(255,0,0)',
                size=10
            ),
            name='news - sell signals'
        )

        py.plot([trace0, trace1, trace2, trace3, trace4], filename='eurusd')

        return

    @staticmethod
    def __timestamp_to_datetime_string(timestamp):
        return timestamp.strftime('%Y-%m-%d %H')
    
    def __get_news_ys(self, prices, news_labels, label_val):
        news_labels = news_labels.loc[news_labels[0] == label_val]

        news_ys = []

        for price_datetime, price in prices.iteritems():

            if not news_labels.loc[news_labels.index == price_datetime].empty:
                news_ys.append(price)
            else:
                news_ys.append(None)

        return news_ys
