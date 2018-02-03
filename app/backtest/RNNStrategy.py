import backtrader as bt
from app.backtest.RNNIndicator import RNNIndicator


class RNNStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),
        ('printlog', True),
    )

    def log(self, txt, dt=None, doprint=False):
        # Logging function for this strategy
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))


    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.data_close = self.datas[0].close
        self.data_predictions = self.datas[0].predictions
        self.datas[0].predictions = None
        # To keep track of pending orders
        self.order = None
        self.buyprice = None
        self.buycomm = None
        # self.sma = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.maperiod)



        # bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        # bt.indicators.WeightedMovingAverage(self.datas[0], period=25).subplot = True
        # bt.indicators.StochasticSlow(self.datas[0])
        # bt.indicators.MACDHisto(self.datas[0])
        # rsi = bt.indicators.RSI(self.datas[0])
        # bt.indicators.SmoothedMovingAverage(rsi, period=10)
        # bt.indicators.ATR(self.datas[0]).plot = False

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.4f, Cost: %.4f, Comm %.4f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.4f, Cost: %.4f, Comm %.4f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceles/Margin/Rejected (' + str(order.status) + ')')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.4f, NET %.4f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # self.log('Close: %.4f - Prediction: %.4f' % (self.data_close[0], self.data_predictions[0]))

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        try:
            # Check if we are in the market
            if not self.position:

                if self.data_predictions[1] > self.data_predictions[0]:
                    self.log('BUY CREATE, %.4f - Prediction: %.4f' % (self.data_close[0], self.data_predictions[1]))

                    # Keep track of the created order to avoid a 2nd order
                    self.order = self.buy()

            else:

                if self.data_predictions[1] < self.data_predictions[0]:
                    self.log('SELL CREATE, %.4f - Prediction: %.4f' % (self.data_close[0], self.data_predictions[1]))

                    # Keep track of the created order to avoid a 2nd order
                    self.order = self.sell()
        except IndexError:
            pass

    # def stop(self):
    #     self.log('(MA Period %2d) Ending Value %.4f' %
    #              (self.params.maperiod, self.broker.getvalue()), doprint=True)
