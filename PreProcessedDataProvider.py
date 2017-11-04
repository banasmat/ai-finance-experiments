import pandas as pd

# TODO rename to PreProcessedDataProvider (?)
class PreProcessedDataProvider(object):

    res_dir = 'resources/'

    def get_price_data(self):
        prices = pd.read_csv(self.res_dir + 'EURUSD.txt', sep=',', dtype=str, usecols=('<DTYYYYMMDD>','<TIME>','<HIGH>','<LOW>'))
        prices.index = pd.to_datetime(prices.pop('<DTYYYYMMDD>') + prices.pop('<TIME>'), format='%Y%m%d%H%M%S')
        prices['mean'] = (pd.to_numeric(prices.pop('<HIGH>')) + pd.to_numeric(prices.pop('<LOW>'))) / 2
        return prices

    def get_news_data(self):
        return pd.read_csv(self.res_dir + 'forex-news.csv', sep=';', dtype=str, usecols=('date','time','symbol','title','actual'))