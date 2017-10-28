import numpy as np
import csv
from datetime import datetime
from collections import Counter
import operator
import re

class ForexAnalyzer(object):

    res_dir = 'resources/'

    news_titles = []

    def __init__(self):
        self.get_data()

    def get_data(self):

        def get_price_datetime(p):
            # TODO time: 'All Day'
            return datetime.strptime(p[0] + p[1], '%Y%m%d%H%M%S')

        def get_price_mean(p):
            return (float(p[2]) + float(p[3])) / 2

        def normalize_news_row(old_row):
            new_row = [0] * 4

            try:
                new_row[0] = get_news_datetime(old_row)
                new_row[1] = get_news_symbol(old_row)
                new_row[2] = get_news_title(old_row)
                new_row[3] = get_actual_value(old_row)
            except ValueError:
                return None

            return new_row

        def get_news_datetime(n):
            return datetime.strptime(n[0] + n[1], '%Y-%m-%d%H:%M').timestamp()

        def get_news_symbol(n):
            return 0 if n[2] == 'EUR' else 1

        def get_news_title(n):
            return self.news_titles.index(n[3]) #TODO consider using a one_hot array

        def get_actual_value(n):

            actual_val = n[4]

            #TODO should get min / max range for every news type

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
            elif '%' in actual_val:
                actual_val = actual_val.replace('%', '')
                actual_val = float(actual_val) * 10**9
            elif '|' in actual_val:
                # TODO not sure if mean is the best approach here
                actual_vals = actual_val.split('|')
                actual_val = (float(actual_vals[0]) + float(actual_vals[1])) / 2
            else:
                actual_val = float(actual_val)


            print(actual_val)

            return actual_val

        prices = np.array(np.genfromtxt(self.res_dir + 'EURUSD.txt', delimiter=',', dtype=str, usecols=(1, 2, 3, 6)))
        prices = dict((get_price_datetime(p), get_price_mean(p)) for p in prices)

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


        print(news[10:])

        news = np.array(news, dtype=np.float32)

        news = map(lambda n: print(n), news[10:])

        # x_normed = (news - news.min(0)) / news.ptp(0)
        # print(x_normed[10:])

        # news_names_counts = sorted(news_names_counts.items(), key=operator.itemgetter(1))
        # print(news_names_counts)
        # for k, v in news_names_counts.items():  # iterating freqa dictionary
        #     print(k + "\t", v)
        i = 0
        # for w in sorted(news_names_counts, key=news_names_counts.get):
        #     print(w, news_names_counts[w])

        # print(len(news_names_counts))

        #TODO do każdego newsa przypisz label : zmiana ceny po godzinie (potem będzie można to zmieniać)

analyzer = ForexAnalyzer()
