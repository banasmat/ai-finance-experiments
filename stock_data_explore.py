import os
from app.dataset.XBRLDataSetProvider import XBRLDataSetProvider
import pandas as pd

# year_file = '2015.csv'
#
# with open(os.path.join(XBRLDataSetProvider.xbrl_dataset_fixed_dir, year_file), 'r') as f:
#     print('YEAR', year_file[0:4])
#     df: pd.DataFrame = pd.read_csv(f, index_col=0)
# print(df.loc[874761].nonzero())

import requests

params = {"formatted": "true",
        "crumb": "AKV/cl0TOgz", # works without so not sure of significance
        "lang": "en-US",
        "region": "US",
        "modules": "defaultKeyStatistics,financialData,calendarEvents",
        "corsDomain": "finance.yahoo.com"}

r = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/GSB", params=params)
data = r.json()[u'quoteSummary']["result"][0]

from pprint import pprint as pp
pp(data)