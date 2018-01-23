from app.live_update.OandaHistoryPriceFetcher import OandaHistoryPriceFetcher
import datetime
from app.dataset.PreProcessedDataProvider import PreProcessedDataProvider
from app.dataset.RNNDatasetProvider import RNNDatasetProvider
from app.keras.KerasRNN import KerasRNN
import matplotlib.pyplot as plt
import numpy as np


def run():

    fetcher = OandaHistoryPriceFetcher()
    prep_data_provider = PreProcessedDataProvider()
    dataset_provider = RNNDatasetProvider()
    nn = KerasRNN()

    lstm_length = 120

    curr_1 = 'EUR'
    curr_2 = 'USD'

    # fetch data for predicting
    _to = datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(minutes=5)
    predict_from = _to - datetime.timedelta(hours=lstm_length+1)

    currency_pair = curr_1 + curr_2

    fetcher.fetch_to_file(predict_from, _to, 'H1', currency_pair)

    # process train data to get right scalers
    prices = prep_data_provider.get_price_records(curr_1, curr_2, [0, 5, 6])
    date_from = datetime.datetime.strptime('2005-01-01 01:00:00', '%Y-%m-%d %H:%M:%S')
    all_prices = prices.loc[(prices.index > date_from) & (prices.index < _to)]
    all_xs, all_ys = dataset_provider.prepare_dataset(all_prices, lstm_length=lstm_length)

    x_test = all_xs[-(lstm_length+1):]
    scaled_predictions = nn.predict(x_test)
    predictions = dataset_provider.unscale_predictions(scaled_predictions)

    y_test = all_ys[-lstm_length:]
    real_prices = dataset_provider.unscale_predictions(y_test)

    # print(prices)
    # print(x_test)
    # quit()

    print(len(real_prices))
    print(len(predictions))

    print(real_prices[-1:])
    print(predictions[-1:])

    plt.plot(real_prices[-10:], color='red', label='Real EURUSD Price')
    plt.plot(predictions[-11:], color='blue', label='Predicted EURUSD Price')
    plt.grid(which='both')
    plt.title('EURUSD Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('EURUSD Price')
    plt.legend()
    plt.show()


run()