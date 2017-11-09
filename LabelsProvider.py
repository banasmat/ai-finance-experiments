import numpy as np
from datetime import timedelta


class LabelsProvider(object):

    def get_labels(self, prices, news, refresh=True):

        if refresh is False:
            labels = np.load('output/labels.npy')
            return labels

        labels = []

        with open('output/notes.txt', 'a') as notes_file:
            for index, n in news.iterrows():

                #TODO might check also larger intervals
                datetime_plus_interval = n['datetime'] + timedelta(hours=12)

                i = 0

                while True:
                    prices_affected_by_news = prices.loc[(prices.index >= n['datetime']) & (prices.index <= datetime_plus_interval)]
                    if i > 100:
                        break
                    elif len(prices_affected_by_news) < 100:
                        datetime_plus_interval += timedelta(hours=12)
                        i += 1
                    else:
                        break

                if i > 100:
                    print('last date: ', n['datetime'])
                    break

                price_when_news_happens = prices_affected_by_news.loc[prices_affected_by_news.index[0]]['mean']

                price_mean_in_affected_period = prices_affected_by_news['mean'].mean()

                diff = price_mean_in_affected_period - price_when_news_happens

                diff_percent = abs((diff / price_when_news_happens) * 100)

                diff_threshold = 0.5
                label = 0
                if diff_percent > diff_threshold:
                    if diff > 0:
                        label = 1
                    else:
                        label = -1

                notes_file.write('news datetime: ' + n['datetime'].strftime('%Y-%m-%d %H%M') + "\n")
                notes_file.write('price when news happens: ' + str(price_when_news_happens) + "\n")
                notes_file.write('label: ' + str(label) + "\n")
                notes_file.write('datetime plus interval: ' + datetime_plus_interval.strftime('%Y-%m-%d %H%M') + "\n")
                notes_file.write('price mean in affected period: ' + str(price_mean_in_affected_period) + "\n")
                notes_file.write('diff: ' + str(diff) + "\n")
                notes_file.write('diff percent: ' + str(diff_percent) + "\n")
                notes_file.write("\n")

                labels.append(label)

        np.save('output/labels.npy', np.array(labels))

        return labels