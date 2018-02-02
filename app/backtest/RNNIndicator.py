import backtrader as bt
from app.keras.KerasRNN import KerasRNN


class RNNIndicator(bt.Indicator):
    lines = ('prediction',)

    params = (
        ('xs', 0),
        ('rnn_dataset_provider', None),
    )

    nn = KerasRNN()

    #TODO params should be dt columns?

    # def __init__(self):
    # TODO get data - how to get last 120 records?
    # prepare data
    # predict data

    def next(self):

        scaled_predictions = self.nn.predict(self.params.xs)
        self.lines.prediction[0] = self.params.rnn_dataset_provider.unscale_predictions(scaled_predictions)


    def once(self, start, end):
       dummy_array = self.lines.dummyline.array

       for i in range(start, end):
           dummy_array[i] = max(0.0, self.params.xs)