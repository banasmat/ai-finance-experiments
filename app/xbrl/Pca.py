from sklearn.preprocessing import StandardScaler
import os
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


class Pca(object):

    xbrl_dataset_dir = os.path.join(os.path.abspath(os.getcwd()), 'output', 'xbrl_dataset')

    def run(self):
        for year_file in reversed(os.listdir(Pca.xbrl_dataset_dir)):
            if year_file[0] == '.':
                continue
            with open(os.path.join(Pca.xbrl_dataset_dir, year_file), 'r') as f:
                print('YEAR', year_file[0:4])
                df: pd.DataFrame = pd.read_csv(f)

                df.fillna(0, inplace=True)

                pca = PCA(n_components=2)
                pca.fit(df)

                print(pca.explained_variance_ratio_)
                first_pc = pca.components_[0]
                second_pc = pca.components_[1]

                transformed_data = pca.transform(df)
                for ii, jj in zip(transformed_data, df):
                    plt.scatter( first_pc[0]*ii[0], first_pc[1]*ii[0], color="r")
                    plt.scatter( second_pc[0]*ii[1], second_pc[1]*ii[1], color="c")
                    plt.scatter( jj[0], jj[1], color="b")

                plt.xlabel('bonus')
                plt.ylabel('long-term incentive')
                plt.show()



                quit()