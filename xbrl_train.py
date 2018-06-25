from app.dataset.XBRLDataSetProvider import XBRLDataSetProvider
import numpy as np
from app.xbrl.XbrlRnn import XbrlRnn

x, y = XBRLDataSetProvider.get_dataset_for_training()
rnn = XbrlRnn()

rnn.train(x, y)