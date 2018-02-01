from app.live_update.OandaHistoryPriceFetcher import OandaHistoryPriceFetcher
import datetime
from app.dataset.PreProcessedDataProvider import PreProcessedDataProvider
from app.dataset.RNNDatasetProvider import RNNDatasetProvider
from app.keras.KerasRNN import KerasRNN
import matplotlib.pyplot as plt
import matplotlib
import numpy as np


def run():

    fetcher = OandaHistoryPriceFetcher()
    prep_data_provider = PreProcessedDataProvider()
    rnn_dataset_provider = RNNDatasetProvider()
    nn = KerasRNN()

    lstm_length = 120

    curr_1 = 'EUR'
    curr_2 = 'USD'

    # fetch data for predicting
    _to = datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(minutes=5)
    predict_from = _to - datetime.timedelta(days=lstm_length)

    gran = 'H1'

    fetcher.fetch_to_file(predict_from, _to)

    # process train data to get right scalers
    prices = prep_data_provider.get_price_records(curr_1, curr_2, ('datetime', 'close', 'high', 'low'), gran)
    date_from = datetime.datetime.strptime('2005-01-01 01:00:00', '%Y-%m-%d %H:%M:%S')
    all_prices = prices.loc[(prices.index > date_from) & (prices.index < _to)]

    all_prices = rnn_dataset_provider.add_news_to_dataset(all_prices, date_from, curr_1, curr_2)
    all_prices = rnn_dataset_provider.enhance_dataset(all_prices)

    all_xs, all_ys = rnn_dataset_provider.prepare_dataset(all_prices, lstm_length=lstm_length)

    x_test = all_xs[-(lstm_length + 1):]
    #x_test = all_xs[-1:]
    scaled_predictions = nn.predict(x_test, gran=gran)
    predictions = rnn_dataset_provider.unscale_predictions(scaled_predictions)

    y_test = all_ys[-lstm_length:]
    real_prices = rnn_dataset_provider.unscale_predictions(y_test)

    dates = prices.loc[(prices.index > (_to - datetime.timedelta(days=20))) & (prices.index < (_to))].index.tolist()
    hours = list(map(lambda date: date.strftime('%d') if date.strftime('%H') == '00' else date.strftime('%H'), dates))

    # _predictions = np.empty(real_prices.shape)
    # _predictions[:] = np.nan
    # predictions = np.append(_predictions, predictions, axis=0)

    show_from = -36

    plt.plot(prices['close'].tolist()[show_from:], color='red', label='Real EURUSD Price')
    plt.plot(predictions[show_from-1:], color='blue', label='Predicted EURUSD Price', marker='o')
    # plt.plot_date(dates, predictions[-31:], color='blue', label='Predicted EURUSD Price')
    plt.grid(which='both')
    plt.title('EURUSD Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('EURUSD Price')
    plt.xticks(np.arange(abs(show_from)+1), prices.index.tolist()[show_from-1:], rotation=90)
    plt.legend()
    plt.show()


run()