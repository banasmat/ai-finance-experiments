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
lstm_length = 120
gran = 'H1'

prices = prep_data_provider.get_price_records(curr_1, curr_2, ('datetime', 'close', 'high', 'low'), gran=gran)
date_from = datetime.datetime.strptime('2005-01-01 01:00:00', '%Y-%m-%d %H:%M:%S')
date_to = datetime.datetime.strptime('2018-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')

prices = rnn_dataset_provider.add_news_to_dataset(prices, date_from, curr_1, curr_2)
prices = rnn_dataset_provider.enhance_dataset(prices)

train_prices = prices.loc[(prices.index > date_from) & (prices.index < date_to)]
x_train, y_train = rnn_dataset_provider.prepare_dataset(train_prices, lstm_length=lstm_length)

nn.train(x_train, y_train, gran)

test_prices = prices.loc[prices.index > (date_to - datetime.timedelta(hours=lstm_length))]
x_test, y_test = rnn_dataset_provider.prepare_dataset(test_prices, lstm_length=lstm_length)
#
scaled_predictions = nn.predict(x_test)
predictions = rnn_dataset_provider.unscale_predictions(scaled_predictions)
real_prices = rnn_dataset_provider.unscale_predictions(y_test)

fig = plt.figure(facecolor='white')

left, width = 0.1, 0.8
rect1 = [left, 0.3, width, 0.4]
rect2 = [left, 0.1, width, 0.2]
rect3 = [left, 0.1, width, 0.2]

ax1 = fig.add_axes(rect1)
ax2 = fig.add_axes(rect2, sharex=ax1)
ax3 = fig.add_axes(rect3, sharex=ax1)

ax1.plot(test_prices['close'].tolist()[-lstm_length:], color='red', label='Real EURUSD Price')
# ax1.plot(test_prices['fibopr_618'].tolist()[-lstm_length:], color='pink', label='FIBOPR_618')
# ax3.plot(test_prices['fibopr_-618'].tolist()[-lstm_length:], color='yellow', label='FIBOPR_-618')
# ax3.plot(test_prices['fibopr_381'].tolist()[-lstm_length:], color='purple', label='FIBOPR_381')
# ax3.plot(test_prices['fibopr_-381'].tolist()[-lstm_length:], color='brown', label='FIBOPR_-381')
ax1.plot(predictions.tolist()[-lstm_length:], color='blue', label='Predicted EURUSD Price')
ax2.plot(test_prices['rsi'].tolist()[-lstm_length:], color='green', label='RSI')
plt.title('EURUSD Price Prediction')
plt.xlabel('Time')
plt.ylabel('EURUSD Price')
plt.legend()
plt.show()
