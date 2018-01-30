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
prices = rnn_dataset_provider.add_rsi_to_dataset(prices)

train_prices = prices.loc[(prices.index > date_from) & (prices.index < date_to)]
x_train, y_train = rnn_dataset_provider.prepare_dataset(train_prices, lstm_length=lstm_length)

nn.train(x_train, y_train, gran)

test_prices = prices.loc[prices.index > (date_to - datetime.timedelta(hours=lstm_length))]
x_test, y_test = rnn_dataset_provider.prepare_dataset(test_prices, lstm_length=lstm_length)

scaled_predictions = nn.predict(x_test)
predictions = rnn_dataset_provider.unscale_predictions(scaled_predictions)
real_prices = rnn_dataset_provider.unscale_predictions(y_test)

print(test_prices)
print(y_test)
# print(real_prices)

plt.plot(test_prices['close'].tolist()[lstm_length:], color='red', label='Real EURUSD Price')
plt.plot(test_prices['rsi'].tolist()[lstm_length:], color='green', label='RSI')
plt.plot(predictions[lstm_length:], color='blue', label='Predicted EURUSD Price')
plt.title('EURUSD Price Prediction')
plt.xlabel('Time')
plt.ylabel('EURUSD Price')
plt.legend()
plt.show()
