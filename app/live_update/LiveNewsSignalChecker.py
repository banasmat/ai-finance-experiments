from app.model.CalendarEntry import CalendarEntry
from app.model.PriceQuote import PriceQuote
from app.database.Connection import Connection

class LiveNewsSignalChecker(object):

    __instance = None

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

        #TODO we have to predict separately for every currency pair separately
        # quotes = session.query(PriceQuote).filter_by(symbol=currency, datetime=dt, title=event).first()

        pass