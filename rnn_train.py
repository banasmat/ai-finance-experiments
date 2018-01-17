from app.dataset.PreProcessedDataProvider import PreProcessedDataProvider
from app.dataset.RNNDatasetProvider import RNNDatasetProvider
from app.keras.KerasRNN import KerasRNN


prep_data_provider = PreProcessedDataProvider()
dataset_provider = RNNDatasetProvider()
nn = KerasRNN()


prices = prep_data_provider.get_price_records('EUR', 'USD', [0, 2,3,4,5,6])

x_train, y_train = dataset_provider.prepare_dataset(prices)

print(x_train)
quit()

nn.train(x_train, y_train)

