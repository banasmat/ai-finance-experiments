import backtrader as bt
from app.backtest.RNNStrategy import RNNStrategy
from app.backtest.PriceData import PriceData
from app.dataset.RNNDatasetProvider import RNNDatasetProvider
from app.keras.KerasRNN import KerasRNN
import numpy
import datetime

from app.dataset.PreProcessedDataProvider import PreProcessedDataProvider


class BackTester(object):

    cerebro = bt.Cerebro()
    prep_data_provider = PreProcessedDataProvider()
    rnn_dataset_provider = RNNDatasetProvider()
    nn = KerasRNN()

    def run(self, date_from, date_to, curr_1='EUR', curr_2='USD', gran='H1'):
        #
        # strats = self.cerebro.optstrategy(
        #     TestStrategy,
        #     maperiod=range(10, 31))

        self.cerebro.addstrategy(RNNStrategy)

        self.cerebro.broker.setcommission(commission=0.001)

        self.cerebro.addsizer(bt.sizers.FixedSize, stake=10)

        lstm_length=120
        prices = self.prep_data_provider.get_price_records(curr_1, curr_2, ('datetime', 'close', 'high', 'low'), gran)
        _prices = self.rnn_dataset_provider.enhance_dataset(prices, date_from, date_to)
        _prices = _prices.loc[(_prices.index > date_from) & (_prices.index < date_to)]
        xs, ys = self.rnn_dataset_provider.prepare_dataset(_prices, lstm_length=lstm_length)

        scaled_predictions = self.nn.predict(xs)

        prices = prices.loc[(prices.index > date_from) & (prices.index < date_to)]
        prices['predictions'] = self.rnn_dataset_provider.unscale_predictions(scaled_predictions)

        data = PriceData(dataname=prices)
        # data = bt.feeds.PandasData(dataname=prices)

        self.cerebro.adddata(data, curr_1 + curr_2)

        self.cerebro.broker.setcash(1000.0)

        print('Starting Portfolio Value: %.2f' % self.cerebro.broker.getvalue())

        self.cerebro.run()

        print('Final Portfolio Value: %.2f' % self.cerebro.broker.getvalue())

        # self.cerebro.plot()