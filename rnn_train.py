from app.dataset.PreProcessedDataProvider import PreProcessedDataProvider
from app.dataset.RNNDatasetProvider import RNNDatasetProvider
from app.keras.KerasRNN import KerasRNN

import matplotlib.pyplot as plt
import datetime


prep_data_provider = PreProcessedDataProvider()
dataset_provider = RNNDatasetProvider()
nn = KerasRNN()


prices = prep_data_provider.get_price_records('EUR', 'USD', [0, 5, 6])
date_from = datetime.datetime.strptime('2005-01-01 01:00:00', '%Y-%m-%d %H:%M:%S')
date_to = datetime.datetime.strptime('2017-12-01 00:00:00', '%Y-%m-%d %H:%M:%S')


train_prices = prices.loc[(prices.index > date_from) & (prices.index < date_to)]
x_train, y_train = dataset_provider.prepare_dataset(train_prices)

# nn.train(x_train, y_train)

test_prices = prices.loc[prices.index > date_to]
x_test, y_test = dataset_provider.prepare_dataset(test_prices)

scaled_predictions = nn.predict(x_test)
predictions = dataset_provider.unscale_predictions(scaled_predictions)

# print(test_prices.tail())
# print(predictions)

plt.plot(y_test, color='red', label='Real EURUSD Price')
plt.plot(predictions, color='blue', label='Predicted EURUSD Price')
plt.title('EURUSD Price Prediction')
plt.xlabel('Time')
plt.ylabel('EURUSD Price')
plt.legend()
plt.show()
