import backtrader as bt


class PriceData(bt.feeds.PandasData):

    params = (('predictions', -1),)
    lines = (('predictions'),)

    def __init__(self):
        self.datafields.append('predictions')
        super(PriceData, self).__init__()
