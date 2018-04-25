# https://www.kaggle.com/dhanyajothimani/basic-visualization-and-clustering-in-python

import time                   # To time processes
import warnings               # To suppress warnings

import numpy as np            # Data manipulation
import pandas as pd           # Dataframe manipulatio
import matplotlib.pyplot as plt                   # For graphics
import seaborn as sns
import plotly.plotly as py #For World Map
import plotly.graph_objs as go
# from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
# init_notebook_mode(connected=True)

from sklearn.preprocessing import StandardScaler  # For scaling dataset
from sklearn.cluster import KMeans, AgglomerativeClustering, AffinityPropagation #For clustering
from sklearn.mixture import GaussianMixture #For GMM clustering
from cluster import KMeansClustering

import os                     # For os related operations
import sys                    # For data size

cols = [
 'AccumulatedDepreciationDepletionAndAmortizationPropertyPlantAndEquipment',
 'Assets',
 'AssetsCurrent',
 'CashAndCashEquivalentsAtCarryingValue',
 'CashAndCashEquivalentsPeriodIncreaseDecrease',
 'CommonStockParOrStatedValuePerShare',
 'CommonStockSharesAuthorized',
 'CommonStockSharesIssued',
 'CommonStockSharesOutstanding',
 'CommonStockValue',
 'EntityCommonStockSharesOutstanding',
 'EntityPublicFloat',
 'IncomeTaxExpenseBenefit',
 'Liabilities',
 'LiabilitiesAndStockholdersEquity',
 'LiabilitiesCurrent',
 'NetIncomeLoss',
 'OperatingIncomeLoss',
 'PropertyPlantAndEquipmentNet',
 'RetainedEarningsAccumulatedDeficit',
 'StockholdersEquity',
]

# Importing the dataset
dataset_path = os.path.join(os.path.abspath(os.getcwd()), 'output', 'xbrl_dataset', '2017.csv')
dataset = pd.read_csv(dataset_path, usecols=cols)
dataset.fillna(0, inplace=True)
# dataset = dataset.transpose() # 'rotate' 90 degrees
# print(dataset)
# cor = dataset.corr() # Correlation of columns
#
# sns.heatmap(cor, square=True) # Plot the correlation as heat map
# plt.subplots_adjust(bottom=0.2, top=1, left=0.07, right=0.87)
# plt.show()

wh1 = dataset.head(100)

ss = StandardScaler()
ss.fit_transform(wh1)

wh1 = [tuple(x) for x in wh1.values]

cl = KMeansClustering(wh1)
clusters = cl.getclusters(3)

print(clusters)