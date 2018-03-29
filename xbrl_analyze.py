from app.dataset.XBRLDataSetProvider import XBRLDataSetProvider
import pandas as pd
import os
import scipy.stats as stats
import pylab as pl
import numpy as np

all_tags = pd.Series()

for quarter_dir in reversed(os.listdir(XBRLDataSetProvider.res_dir)):

    quarter_dir = os.path.join(XBRLDataSetProvider.res_dir, quarter_dir)

    if not os.path.isdir(quarter_dir):
        continue

    num_file = os.path.join(quarter_dir, 'num.txt')
    numbers = pd.read_csv(num_file, sep='\t', encoding='ISO-8859-1', usecols=['tag'])
    all_tags = all_tags.append(numbers)
    break

all_tags = all_tags.groupby(['tag'])['tag'].count()
all_tags = all_tags.sort_values(ascending=True)
all_tags = all_tags[(all_tags >= 20000)].index.unique().tolist()
print(all_tags)
quit()
# print(np.percentile(h, 50))
print(np.mean(all_tags))
print(np.median(all_tags))
print(np.std(all_tags))
fit = stats.norm.pdf(all_tags, np.mean(all_tags), np.std(all_tags))  # this is a fitting indeed

# xticks = np.arange(0, max(all_tags), 1000)

pl.plot(all_tags, fit, '-o')

pl.hist(all_tags, normed=True)  # use this to draw histogram of your data
# pl.xticks(np.arange(0, max(all_tags), 1000))
pl.show()

