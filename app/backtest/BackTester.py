import backtrader as bt
from app.backtest.RNNStrategy import RNNStrategy
from app.backtest.ReinforcementStrategy import ReinforcementStrategy
from app.backtest.PriceData import PriceData
from app.dataset.RNNDatasetProvider import RNNDatasetProvider
from app.keras.KerasRNN import KerasRNN
import pandas as pd
import matplotlib.pyplot as plt
import os

from app.dataset.PreProcessedDataProvider import PreProcessedDataProvider


class BackTester(object):

    cerebro = bt.Cerebro()
    prep_data_provider = PreProcessedDataProvider()
    rnn_dataset_provider = RNNDatasetProvider()
    nn = KerasRNN()

    def run(self, date_from, date_to, curr_1='EUR', curr_2='USD', gran='H1'):
        #
        # strats = self.cerebro.optstrategy(
        #     RNNStrategy,
        #     maperiod=[10])

        # self.cerebro.addstrategy(RNNStrategy)
        self.cerebro.addstrategy(ReinforcementStrategy)

        self.cerebro.broker.setcommission(commission=0.001)

        self.cerebro.addsizer(bt.sizers.PercentSizer, percents=10)

        lstm_length = 120
        prices = self.prep_data_provider.get_price_records(curr_1, curr_2, ('datetime', 'open', 'high', 'low', 'close', 'volume'), gran)
        _prices: pd.DataFrame = prices.copy()
        _prices.drop(['open', 'volume'], axis=1, inplace=True)
        _prices = self.rnn_dataset_provider.enhance_dataset(_prices, date_from, date_to)
        _prices = _prices.loc[(_prices.index > date_from) & (_prices.index < date_to)]
        xs, ys = self.rnn_dataset_provider.prepare_dataset(_prices, lstm_length=lstm_length)

        scaled_predictions = self.nn.predict(xs)

        prices = prices.loc[(prices.index > date_from) & (prices.index < date_to)]
        prices['predictions'] = self.rnn_dataset_provider.unscale_predictions(scaled_predictions)

        prices.fillna(1, inplace=True)

        data = PriceData(dataname=prices)

        self.cerebro.adddata(data, curr_1 + curr_2)

        scores = []
        rng = range(0, 10)
        for i in rng:
            self.cerebro.broker.setcash(1000.0)
            print('Starting Portfolio Value: %.2f' % self.cerebro.broker.getvalue())

            self.cerebro.run()

            print('Final Portfolio Value: %.2f' % self.cerebro.broker.getvalue())
            scores.append(self.cerebro.broker.getvalue())
        # self.cerebro.plot()

        with open(os.path.join(os.path.abspath(os.getcwd()), 'output', 'brain-scores.txt'), "r") as f:
            brain_scores = f.read().split(',')

        plt.subplot(2, 1, 1)
        plt.plot(brain_scores)
        plt.title('Brain scores')

        plt.subplot(2, 1, 2)
        plt.plot(rng, scores)
        plt.xlabel('iterations')
        plt.ylabel('Portfolio values')

        plt.show()