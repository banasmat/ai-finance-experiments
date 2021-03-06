from typing import List

import numpy as np
from datetime import timedelta
import pandas as pd


class LabelsProvider(object):

    def get_labels(self, prices: pd.DataFrame, news: pd.DataFrame) -> np.ndarray:

        labels = []

        # with open('output/notes.txt', 'a') as notes_file:
        for index, n in news.iterrows():

            #TODO might check also larger intervals
            datetime_plus_interval = n['datetime'] + timedelta(hours=12)

            i = 0

            while True:
                prices_affected_by_news = prices.loc[(prices.index >= n['datetime']) & (prices.index <= datetime_plus_interval)]
                if i > 100:
                    break
                elif len(prices_affected_by_news) < 2:
                    datetime_plus_interval += timedelta(hours=12)
                    i += 1
                else:
                    break

            if i > 100:
                break

            price_when_news_happens = prices_affected_by_news['mean'][0]

            price_mean_in_affected_period = prices_affected_by_news.mean()[0]

            diff = price_mean_in_affected_period - price_when_news_happens

            label = self.get_diff_label(diff, price_when_news_happens)

            # notes_file.write('news datetime: ' + n['datetime'].strftime('%Y-%m-%d %H%M') + "\n")
            # notes_file.write('price when news happens: ' + str(price_when_news_happens) + "\n")
            # notes_file.write('label: ' + str(label) + "\n")
            # notes_file.write('datetime plus interval: ' + datetime_plus_interval.strftime('%Y-%m-%d %H%M') + "\n")
            # notes_file.write('price mean in affected period: ' + str(price_mean_in_affected_period) + "\n")
            # notes_file.write('diff: ' + str(diff) + "\n")
            # # notes_file.write('diff percent: ' + str(diff_percent) + "\n")
            # notes_file.write("\n")

            labels.append(label)

        labels = np.array(labels)

        return labels

    @staticmethod
    def get_diff_label(diff, price_when_news_happens) -> int:

        diff_percent = (diff / price_when_news_happens) * 100

        if diff_percent > 1.:
            label = 1
        elif diff_percent > 0.5:
            label = 0.5
        elif diff_percent > -0.5:
            label = 0
        elif diff_percent > -1.:
            label = -0.5
        else:
            label = -1

        return label

    @staticmethod
    def get_all_labels() -> List:
        return list(range(-2, 3, 1))
