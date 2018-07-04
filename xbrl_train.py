from app.dataset.XBRLDataSetProvider import XBRLDataSetProvider
from app.xbrl.XbrlRnn import XbrlRnn

x, y = XBRLDataSetProvider.get_dataset_for_training()
x, y = XBRLDataSetProvider.scale_by_cik_tag(x, y)

rnn = XbrlRnn()
rnn.train(x[:-1], y[:-1])



predictions = rnn.predict(x[-1:])
print(predictions[0])
print(y[-1:][0])
accuracy = len(set(predictions[0].tolist()) & set(y[-1:][0].tolist())) / len(predictions[0])
print('accuracy',accuracy)


#TODO
# nie puszczać cików razem tylko osobno (?) - tracimy continuum, ale lepsze to niż nic
# LUB
# https://datascience.stackexchange.com/questions/27563/multi-dimentional-and-multivariate-time-series-forecast-rnn-lstm-keras
#
# trzeba jakoś odczytać predictions
# wypluć tabelkę wyników: Symbol/cik : wynik
#
# Model:
# relu ?
# więcej neuronów
#
# Dane:
# jeśli zero jest pomiędzy innymi wartościami, brać poprzednią

