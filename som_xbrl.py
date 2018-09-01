# https://github.com/JustGlowing/minisom/blob/master/examples/examples.ipynb

from minisom import MiniSom
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

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

data = dataset

# Initialization and training
som = MiniSom(7, 7, 4, sigma=1.0, learning_rate=0.5)
som.random_weights_init(data)
print("Training...")
som.train_random(data, 100)  # random training
print("\n...ready!")