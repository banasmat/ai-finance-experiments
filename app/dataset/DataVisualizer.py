from datetime import datetime

import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly as plotly
import plotly.graph_objs as go


class DataVisualizer(object):

    def __init__(self):
        plotly.tools.set_credentials_file(username='banasmat', api_key='La513i6uVpqf7qAHQnCD')

    def visualize(self, prices, news, labels, filename, show_zeros=True):

        news = news.iloc[:len(labels)]
        news_labels = pd.DataFrame(labels)

        news_labels.index = news['datetime'].dt.round('h')

        prices = prices.resample('1H').mean()

        price_xs = prices.index.tolist()
        price_ys = prices.values.tolist()

        price_xs = list(map(self.__timestamp_to_datetime_string, price_xs))

        news_zero_ys = self.__get_news_ys(prices, news_labels, 0)
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
        trace5 = go.Scattergl(
            x=np.array(price_xs),
            y=np.array(news_zero_ys),
            mode='markers',
            marker=dict(
                color='rgb(0,0,0)',
                size=10
            ),
            name='news - no movement signals'
        )

        plots = [trace0, trace1, trace2, trace3, trace4]

        if show_zeros:
            plots.add(trace5)

        py.plot(plots, filename=filename)

        return

    @staticmethod
    def __timestamp_to_datetime_string(timestamp):
        return timestamp.strftime('%Y-%m-%d %H')

    def __get_news_ys(self, prices, news_labels, label_val):
        news_labels = news_labels.loc[news_labels[0] == label_val]

        news_ys = []

        for price_datetime, price in prices.iterrows():
            #
            # if isinstance(price_datetime, str) or np.math.isnan(price):
            #     continue

            if not news_labels.loc[news_labels.index == price_datetime].empty:
                news_ys.append(price[0])
            else:
                news_ys.append(None)

        return news_ys
