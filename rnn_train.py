from app.dataset.PreProcessedDataProvider import PreProcessedDataProvider
from app.dataset.RNNDatasetProvider import RNNDatasetProvider
from app.keras.KerasRNN import KerasRNN
import datetime


prep_data_provider = PreProcessedDataProvider()
dataset_provider = RNNDatasetProvider()
nn = KerasRNN()


prices = prep_data_provider.get_price_records('EUR', 'USD', [0, 5, 6])
date_from = datetime.datetime.strptime('2005-01-01 01:00:00', '%Y-%m-%d %H:%M:%S')
date_to = datetime.datetime.strptime('2017-12-01 00:00:00', '%Y-%m-%d %H:%M:%S')


train_prices = prices.loc[(prices.index > date_from) & (prices.index < date_to)]
x_train, y_train = dataset_provider.prepare_dataset(train_prices)

nn.train(x_train, y_train)

# test_prices = prices.loc[prices.index > date_until]
# x_test, y_test = dataset_provider.prepare_dataset(test_prices)



