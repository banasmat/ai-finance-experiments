from sklearn.preprocessing import StandardScaler
import os
import pandas as pd
import numpy as np


class Pca(object):

    xbrl_dataset_dir = os.path.join(os.path.abspath(os.getcwd()), 'output', 'xbrl_dataset')

    def run(self):
        for year_file in reversed(os.listdir(Pca.xbrl_dataset_dir)):
            if year_file[0] == '.':
                continue
            with open(os.path.join(Pca.xbrl_dataset_dir, year_file), 'r') as f:
                print('YEAR', year_file[0:4])
                df: pd.DataFrame = pd.read_csv(f)