from datetime import timedelta
import pandas as pd


class FeatureProvider:

    @staticmethod
    def add_preceding_price_feature(prices, news, refresh=True):

        if refresh is not True:
            return pd.DataFrame.from_csv('output/feat_news.csv')

        news['preceding_price'] = pd.Series()

        for index, n in news.iloc[::-1].iterrows():

            # TODO code duplication with label provider
            datetime_minus_interval = n['datetime'] - timedelta(hours=12)

            i = 0

            while True:
                prices_preceding_news = prices.loc[
                    (prices.index < n['datetime']) & (prices.index >= datetime_minus_interval)]
                if i > 100:
                    break
                elif len(prices_preceding_news) < 100:
                    datetime_minus_interval -= timedelta(hours=12)
                    i += 1
                else:
                    break

            if i > 100:
                print('last date: ', n['datetime'])
                break

            price_when_news_happens = prices_preceding_news.loc[prices_preceding_news.index[-1]]['mean']

            price_mean_in_affected_period = prices_preceding_news['mean'].mean()

            diff = price_mean_in_affected_period - price_when_news_happens

            diff_percent = abs((diff / price_when_news_happens) * 100)

            diff_threshold = 0.5
            feature = 0
            if diff_percent > diff_threshold:
                if diff > 0:
                    feature = 1
                else:
                    feature = -1

            news.loc[news['datetime'] == n['datetime'], 'preceding_price'] = feature

        news.to_csv('output/feat_news.csv')

        return news
