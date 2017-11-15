from datetime import timedelta
import pandas as pd
from LabelsProvider import LabelsProvider


class FeatureProvider:

    def add_preceding_price_feature(self, prices, news: pd.DataFrame, pair: str, refresh=True) -> pd.DataFrame:

        filename = 'output/feat_news_' + pair + '.csv'

        if refresh is not True:
            return pd.read_csv(filename, parse_dates=['datetime'])

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
                break

            price_when_news_happens = prices_preceding_news.loc[prices_preceding_news.index[-1]]['mean']

            price_mean_in_affected_period = prices_preceding_news['mean'].mean()

            diff = price_mean_in_affected_period - price_when_news_happens

            feature = LabelsProvider.get_diff_label(diff, price_when_news_happens)

            news.loc[news['datetime'] == n['datetime'], 'preceding_price'] = feature

        news.to_csv(filename)

        return news

