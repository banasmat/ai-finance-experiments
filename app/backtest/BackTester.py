import backtrader as bt
from app.backtest.TestStrategy import TestStrategy
from app.backtest.PriceData import PriceData
import numpy
import datetime

from app.dataset.PreProcessedDataProvider import PreProcessedDataProvider


class BackTester(object):

    cerebro = bt.Cerebro()
    prep_data_provider = PreProcessedDataProvider()

    def run(self, date_from, date_to, curr_1='EUR', curr_2='USD', gran='H1'):

        strats = self.cerebro.optstrategy(
            TestStrategy,
            maperiod=range(10, 31))

        self.cerebro.broker.setcommission(commission=0.001)

        self.cerebro.addsizer(bt.sizers.PercentSizer, percents=10)

        prices = self.prep_data_provider.get_price_records(curr_1, curr_2, ('datetime', 'open', 'high', 'low', 'close', 'volume'), gran=gran)
        prices = prices.loc[(prices.index > date_from) & (prices.index < date_to)]

        prices['test'] = 1

        data = PriceData(dataname=prices)

        self.cerebro.adddata(data, curr_1 + curr_2)

        self.cerebro.broker.setcash(1000.0)

        print('Starting Portfolio Value: %.2f' % self.cerebro.broker.getvalue())

        self.cerebro.run()

        print('Final Portfolio Value: %.2f' % self.cerebro.broker.getvalue())

        # self.cerebro.plot()