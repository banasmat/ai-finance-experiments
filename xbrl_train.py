from app.dataset.XBRLDataSetProvider import XBRLDataSetProvider
from app.xbrl.XbrlRnn import XbrlRnn

x, y = XBRLDataSetProvider.get_dataset_for_training()
x, y = XBRLDataSetProvider.scale_by_cik_tag(x, y)

rnn = XbrlRnn()
rnn.train(x[:-1], y[:-1])



predictions = rnn.predict(x[-1:])
# print(predictions[0])
# print(y[-1:][0])
predictions = list(map(lambda x: 0 if x < 0.5 else 1, predictions[0].tolist()))
print(predictions)

test_vals = y[-1:][0].tolist()
print(test_vals)
correct_predictions = 0
for i in range (0, len(predictions)):
    if predictions[i] == test_vals[i]:
        correct_predictions += 1


# accuracy = len(set(predictions) & set(y[-1:][0].tolist())) / len(predictions)
print('accuracy',correct_predictions/len(predictions))


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
#
# UWAGA: sprawdzić czy nie trzeba przesunąć danych w Y o 1 (czy chcemy brać wynik z tego roku czy z nastepnego)


