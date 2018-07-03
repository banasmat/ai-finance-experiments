from app.dataset.XBRLDataSetProvider import XBRLDataSetProvider
from app.xbrl.XbrlRnn import XbrlRnn

x, y = XBRLDataSetProvider.get_dataset_for_training()
x, y = XBRLDataSetProvider.scale_by_cik_tag(x, y)

rnn = XbrlRnn()
rnn.train(x, y)




#TODO
# nie puszczać cików razem tylko osobno (?) - tracimy continuum, ale lepsze to niż nic
#
# LUB
# https://datascience.stackexchange.com/questions/27563/multi-dimentional-and-multivariate-time-series-forecast-rnn-lstm-keras
#
# trzeba jakoś odczytać predictions

# rnn.predict(x)