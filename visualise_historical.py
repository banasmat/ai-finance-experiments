from app.dataset.DataSetProvider import DataSetProvider
from app.dataset.DataVisualizer import DataVisualizer
from app.dataset.PreProcessedDataProvider import PreProcessedDataProvider
from app.dataset.LabelsProvider import LabelsProvider

def run():
    prep_data_provider = PreProcessedDataProvider()
    data_set_provider = DataSetProvider()
    data_visualizer = DataVisualizer()
    labels_provider = LabelsProvider()

    currency_pair = 'EURUSD'
    # currency_pair = 'EURCAD'
    # currency_pair = 'AUDJPY'

    curr_1 = currency_pair[:3]
    curr_2 = currency_pair[-3:]

    prices = prep_data_provider.get_price_data(curr_1, curr_2)
    news = prep_data_provider.get_news_data(prices.index[0], curr_1, curr_2)

    # price_news_map[currency_pair]['news'] = prep_data_provider.scale_news_data(price_news_map[currency_pair]['news'])

    labels = labels_provider.get_labels(prices, news)

    # prices = prices.fillna(0)

    data_visualizer.visualize(prices, news, labels, currency_pair + '_hist', show_zeros=False)


run()
