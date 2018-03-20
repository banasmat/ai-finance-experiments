import backtrader as bt

from app.reinforcement.ai import Dqn
import matplotlib.pyplot as plt
import os

class ReinforcementStrategy(bt.Strategy):
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
        # To keep track of pending orders
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.brain = Dqn(6,3,0.9)
        self.brain.load()
        self.last_reward = 0
        self.last_value = self.broker.getvalue()
        self.scores = []

        self.sma = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.maperiod)
        self.ema = bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        self.wma = bt.indicators.WeightedMovingAverage(self.datas[0], period=25)
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

                self.last_reward = -0.1

            else:  # Sell
                self.log('SELL EXECUTED, Price: %.4f, Cost: %.4f, Comm %.4f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
                pass

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            # self.log('Order Canceled/Margin/Rejected (' + str(order.status) + ')')
            pass

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.4f, NET %.4f' %
                 (trade.pnl, trade.pnlcomm))

        if trade.pnlcomm > 1:
            self.last_reward = 0.5
        elif trade.pnlcomm > 0:
            self.last_reward = 0.1
        elif trade.pnlcomm < -1:
            self.last_reward = -1
        else:
            self.last_reward = -0.8

    def _get_market_action(self, action):

        if action == 0:
            return None
        if action == 1 and not self.position: # and if not self.position:
            return self.buy
        if action == 2 and self.position:
            return self.sell
        return None

    def next(self):
        # self.log('Close: %.4f - Prediction: %.4f' % (self.data_close[0], self.data_predictions[0]))

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        is_trade_opened = 0
        if self.position:
            is_trade_opened = 1

        last_signal = [self.data_close[0], self.data_predictions[0], self.sma[0], self.ema[0], self.wma[0], is_trade_opened]
        action = self.brain.update(self.last_reward, last_signal)

        self.scores.append(self.brain.score())
        with open(os.path.join(os.path.abspath(os.getcwd()), 'output', 'brain-scores.txt'), "a") as f:
            f.write("%.2f," % self.brain.score())
        market_action = self._get_market_action(action)
        if market_action is not None:
            self.order = market_action()

        value = self.broker.getvalue()
        # delta = value - self.last_value
        #
        # if delta > 0:
        #     self.last_reward = 0.2
        # else:
        #     self.last_reward = -0.2

        self.last_value = value

        try:
            self.data_close[1]
        except IndexError:
            self.stop()

    def stop(self):
        # self.log('(MA Period %2d) Ending Value %.4f' %
        #          (self.params.maperiod, self.broker.getvalue()), doprint=True)

        self.brain.save()
        # plt.plot(self.scores)
        # plt.show()
