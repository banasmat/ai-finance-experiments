import backtrader as bt


class PriceData(bt.feeds.PandasData):

    params = (('test', -1),)
    lines = (('test'),)

    def __init__(self):
        self.datafields.append('test')
        super(PriceData, self).__init__()
