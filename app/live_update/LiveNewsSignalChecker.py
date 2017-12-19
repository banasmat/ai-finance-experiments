from app.model.CalendarEntry import CalendarEntry
from app.model.PriceQuote import PriceQuote
from app.model.Signal import Signal
from app.database.Connection import Connection
from app.dataset.PreProcessedDataProvider import PreProcessedDataProvider
from app.dataset.DataSetProvider import DataSetProvider
from app.keras.KerasNeuralNetwork import KerasNeuralNetwork
import datetime


class LiveNewsSignalChecker(object):

    __instance = None

    __all_currency_pairs = None

    # TODO we should be using some dependency injection (or singletons ?)
    data_set_provider = DataSetProvider()
    nn = KerasNeuralNetwork()

    @staticmethod
    def get_instance():
        """ Static access method. """
        if LiveNewsSignalChecker.__instance is None:
            LiveNewsSignalChecker()
        return LiveNewsSignalChecker.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if LiveNewsSignalChecker.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            LiveNewsSignalChecker.__instance = self

    def check(self, calendar_entry: CalendarEntry):

        session = Connection.get_instance().get_session()

        # 64 hours should contain sufficient margin
        quotes_since = calendar_entry.datetime - datetime.timedelta(hours=64)

        if self.__all_currency_pairs is None:
            self.__all_currency_pairs = PreProcessedDataProvider.get_currency_pair_strings()

        currency_pairs = list(filter(lambda currency_pair: calendar_entry.currency in currency_pair, self.__all_currency_pairs))

        for symbol in currency_pairs:
            quotes = session.query(PriceQuote)\
                .filter_by(symbol=symbol)\
                .filter(PriceQuote.datetime >= quotes_since).all()

            data_set = self.data_set_provider.prepare_single_data_set(calendar_entry, quotes, symbol)

            prediction = self.nn.predict(data_set[0])
            # print(prediction)
            # quit()

            signal = Signal(prediction, symbol, calendar_entry)
            session.add(signal)

        session.commit()
