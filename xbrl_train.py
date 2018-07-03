from app.dataset.XBRLDataSetProvider import XBRLDataSetProvider
import numpy as np
from app.xbrl.XbrlRnn import XbrlRnn

x, y = XBRLDataSetProvider.get_dataset_for_training()
rnn = XbrlRnn()

# cik, tag, year
x = x.transpose((1, 2, 0))
# cik, year
y = y.transpose()

for cik_index in range(0, x.shape[0]):
    x[cik_index] = XBRLDataSetProvider.scale_dataset(x[cik_index])
    x[cik_index] = np.nan_to_num(x[cik_index])

# rnn.train(cik_data, y[cik_index])



# rnn.predict(x)