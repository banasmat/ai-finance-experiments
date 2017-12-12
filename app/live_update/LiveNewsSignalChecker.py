from app.model.CalendarEntry import CalendarEntry
from app.model.PriceQuote import PriceQuote
from app.database.Connection import Connection
from app.dataset.PreProcessedDataProvider import PreProcessedDataProvider
import datetime


class LiveNewsSignalChecker(object):

    __instance = None

    __all_symbols = None

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

        #TODO what if quotes are missing ? like event occured monday morning
        quotes_since = calendar_entry.datetime - datetime.timedelta(hours=12)

        if self.__all_symbols is None:
            self.__all_symbols = PreProcessedDataProvider.get_symbol_pair_strings()

        symbols = list(filter(lambda symbol: calendar_entry.currency in symbol, self.__all_symbols))

        quotes_map = {}

        for symbol in symbols:
            quotes_map[symbol] = session.query(PriceQuote)\
                .filter_by(symbol=symbol)\
                .filter(PriceQuote.datetime >= quotes_since).all()



        print(calendar_entry.currency)
        print(quotes_map)
        quit()

        pass
