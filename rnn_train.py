from app.dataset.PreProcessedDataProvider import PreProcessedDataProvider
from app.dataset.RNNDatasetProvider import RNNDatasetProvider
from app.dataset.DataSetProvider import DataSetProvider
from app.keras.KerasRNN import KerasRNN

import matplotlib.pyplot as plt
import datetime
import pandas as pd
import numpy as np


prep_data_provider = PreProcessedDataProvider()
rnn_dataset_provider = RNNDatasetProvider()
data_set_provider = DataSetProvider()
nn = KerasRNN()

curr_1 = 'EUR'
curr_2 = 'USD'

prices = prep_data_provider.get_price_records(curr_1, curr_2, ('datetime', 'close', 'high', 'low'), gran='D1')
date_from = datetime.datetime.strptime('2005-01-01 01:00:00', '%Y-%m-%d %H:%M:%S')
date_to = datetime.datetime.strptime('2018-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')

lstm_length = 120
gran = 'H1'

news = prep_data_provider.get_news_data(date_from, curr_1, curr_2)
news = prep_data_provider.scale_news_data(news)

all_titles = prep_data_provider.get_all_titles()
news.index = news['datetime'].dt.round('h')
news: pd.DataFrame = news.drop(['symbol', 'symbol_pair', 'title'], axis=1)
# news = data_set_provider.one_hot_from_all_items(news, 'title', all_titles)

prices.loc[:, 'actual'] = 0
prices.loc[:, 'forecast'] = 0
prices.loc[:, 'previous'] = 0

for dt, price in prices.iterrows():
    news_during_dt = news.loc[news.index == dt]
    if len(news_during_dt) > 0:
        prices.loc[dt, 'actual'] = news_during_dt['actual'].mean()
        prices.loc[dt, 'forecast'] = news_during_dt['forecast'].dropna().mean()
        prices.loc[dt, 'previous'] = news_during_dt['previous'].dropna().mean()

prices.fillna(0, inplace=True)
train_prices = prices.loc[(prices.index > date_from) & (prices.index < date_to)]
x_train, y_train = rnn_dataset_provider.prepare_dataset(train_prices, lstm_length=lstm_length)

nn.train(x_train, y_train, gran)

test_prices = prices.loc[prices.index > (date_to - datetime.timedelta(hours=lstm_length))]
x_test, y_test = rnn_dataset_provider.prepare_dataset(test_prices, lstm_length=lstm_length)

scaled_predictions = nn.predict(x_test)
predictions = rnn_dataset_provider.unscale_predictions(scaled_predictions)
real_prices = rnn_dataset_provider.unscale_predictions(y_test)

plt.plot(real_prices, color='red', label='Real EURUSD Price')
plt.plot(predictions, color='blue', label='Predicted EURUSD Price')
plt.title('EURUSD Price Prediction')
plt.xlabel('Time')
plt.ylabel('EURUSD Price')
plt.legend()
plt.show()
