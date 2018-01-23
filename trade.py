from app.live_update.OandaHistoryPriceFetcher import OandaHistoryPriceFetcher
import datetime
from app.dataset.PreProcessedDataProvider import PreProcessedDataProvider
from app.dataset.RNNDatasetProvider import RNNDatasetProvider
from app.keras.KerasRNN import KerasRNN
import matplotlib.pyplot as plt


def run():

    fetcher = OandaHistoryPriceFetcher()
    prep_data_provider = PreProcessedDataProvider()
    dataset_provider = RNNDatasetProvider()
    nn = KerasRNN()

    lstm_length = 120

    curr_1 = 'EUR'
    curr_2 = 'USD'

    # process train data to get right scalers
    # TODO save scaler to file instead
    prices = prep_data_provider.get_price_records(curr_1, curr_2, [0, 5, 6])
    date_from = datetime.datetime.strptime('2005-01-01 01:00:00', '%Y-%m-%d %H:%M:%S')
    date_to = datetime.datetime.now() - datetime.timedelta(weeks=4)
    train_prices = prices.loc[(prices.index > date_from) & (prices.index < date_to)]
    x_train, y_train = dataset_provider.prepare_dataset(train_prices, lstm_length=lstm_length)
    #
    # print(train_prices)
    # print(x_train)

    # fetch data for predicting
    _to = datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(minutes=5)
    _from = _to - datetime.timedelta(hours=lstm_length+1)

    currency_pair = curr_1 + curr_2

    prices = fetcher.fetch_to_file(_from, _to, 'H1', currency_pair)

    quit()

    prices.drop(['open', 'high', 'low'], axis=1, inplace=True)
    x_test, y_test = dataset_provider.prepare_dataset(prices, lstm_length=lstm_length)

    # print(prices)
    # print(x_test)
    # quit()

    scaled_predictions = nn.predict(x_test)

    print(scaled_predictions[0])

    # print(scaled_predictions)
    quit()
    predictions = dataset_provider.unscale_predictions(scaled_predictions)

    real_prices = dataset_provider.unscale_predictions(y_test)

    plt.plot(real_prices, color='red', label='Real EURUSD Price')
    plt.plot(predictions, color='blue', label='Predicted EURUSD Price')
    plt.title('EURUSD Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('EURUSD Price')
    plt.legend()
    plt.show()


run()