import numpy as np
import csv
from datetime import datetime, timedelta
from collections import Counter
import operator
import re

class ForexAnalyzer(object):

    res_dir = 'resources/'

    news_titles = []
    scale_map = {}

    def __init__(self):
        self.get_data()

    def get_data(self):

        def get_price_datetime(p):
            # TODO time: 'All Day'
            return datetime.strptime(p[0] + p[1], '%Y%m%d%H%M%S').timestamp()

        def get_price_mean(p):
            return (float(p[2]) + float(p[3])) / 2

        def normalize_news_row(old_row):
            new_row = [0] * 4

            try:
                new_row[0] = get_news_datetime(old_row)
                new_row[1] = get_news_symbol(old_row)
                new_row[2] = get_news_title(old_row)
                new_row[3] = get_actual_value(old_row)
                update_scale_map(new_row)
            except ValueError:
                return None

            return new_row

        def get_news_datetime(n):
            return datetime.strptime(n[0] + n[1], '%Y-%m-%d%H:%M') #.timestamp()

        def get_news_symbol(n):
            return 0 if n[2] == 'EUR' else 1

        def get_news_title(n):
            return self.news_titles.index(n[3]) #TODO consider using a one_hot array

        def get_actual_value(n):

            actual_val = n[4]

            if actual_val == '':
                raise ValueError('News Actual value is empty')
            elif 'K' in actual_val:
                actual_val = actual_val.replace('M', '')
                actual_val = float(actual_val) * 10**3
            elif 'M' in actual_val:
                actual_val = actual_val.replace('M', '')
                actual_val = float(actual_val) * 10**6
            elif 'B' in actual_val:
                actual_val = actual_val.replace('B', '')
                actual_val = float(actual_val) * 10**9
            elif 'T' in actual_val:
                actual_val = actual_val.replace('T', '')
                actual_val = float(actual_val) * 10**12
            elif '%' in actual_val:
                actual_val = actual_val.replace('%', '')
                actual_val = actual_val.replace('<', '')
                actual_val = float(actual_val) / 100
            elif '|' in actual_val:
                # TODO not sure if mean is the best approach here
                actual_vals = actual_val.split('|')
                actual_val = (float(actual_vals[0]) + float(actual_vals[1])) / 2
            else:
                actual_val = float(actual_val)

            return actual_val

        def update_scale_map(new_row):
            if new_row[2] in self.scale_map.keys():
                self.scale_map[new_row[2]].append(new_row[3])
            else:
                self.scale_map[new_row[2]] = []

        def reduce_to_min_and_max(tuple):
            return tuple[0], [min(tuple[1]), max(tuple[1])]

        def scale_values(row):
            row[3] -= self.scale_map[row[2]][0]
            row[3] /= self.scale_map[row[2]][1]
            return row

        # FIXME Memory Error. We dont' have to load all of these to memory. We should search in csv when its' needed (or use db) https://stackoverflow.com/questions/26082360/python-searching-csv-and-return-entire-row
        prices = np.array(np.genfromtxt(self.res_dir + 'EURUSD.txt', delimiter=',', dtype=str, usecols=(1, 2, 3, 6)))
        prices = dict((get_price_datetime(p), get_price_mean(p)) for p in reversed(prices))

        news = []

        with open(self.res_dir + 'forex-news.csv') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';')

            # time_regex = re.compile('\d+?:\d{2}')

            for row in csv_reader:
                # row[1] = time, some are strings like 'All Day' #TODO think how to handle All Day
                # row[4] = 'actual' value
                if row[2] in ['EUR', 'USD']: # and row[4] != '' and time_regex.match(row[1]):
                    news.append(row)

        news_names_counts = dict(Counter(list(map(lambda n: n[3], news))))

        for k, v in news_names_counts.items():
            if v >= 100:
                self.news_titles.append(k)

        news = list(map(normalize_news_row, news))
        news = list(filter(lambda n: n is not None, news))

        self.scale_map = dict(map(reduce_to_min_and_max, self.scale_map.items()))
        news = list(map(scale_values, news))
        print(news[-1:])

        # news = np.array(news, dtype=np.float32)

        # np.set_printoptions(suppress=True, precision=3)
        # print(news[-1:])

        labels = []

        for k,v in prices.items():
            print(k)
            # quit()

        for n in reversed(news):
            #TODO might check also larger intervals
            datetime_plus_interval = n[0] + timedelta(hours=1)
            news_datetime = n[0]
            price_when_news_happens = None

            print('news_datetime', news_datetime.timestamp())

            while True:
                try:

                    price_when_news_happens = prices[news_datetime.timestamp()]
                    break
                except KeyError:
                    if (news_datetime - n[0]).days > 3:
                        break
                    else:
                        news_datetime += timedelta(minutes=1)
            print(news_datetime)
            if price_when_news_happens is None:
                break

            while True:
                try:
                    # TODO scale ?
                    labels.append(price_when_news_happens - prices[datetime_plus_interval])
                    break
                except KeyError:
                    if (datetime_plus_interval - n[0]).days > 3:
                        break
                    else:
                        datetime_plus_interval += timedelta(hours=1)

        #TODO remove datetime col
        #TODO separate to train_x, train_y, test_x, test_y



        print(labels[:10])

analyzer = ForexAnalyzer()
