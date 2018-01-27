from sqlalchemy.orm import aliased

from app.live_update.NewsScrapper import NewsScrapper
from app.live_update.LiveNewsSignalChecker import LiveNewsSignalChecker
import datetime
from app.event.CalendarEventSubscriber import CalendarEventSubscriber
from app.model.CalendarEntry import CalendarEntry
from app.model.Signal import Signal
from app.database.Connection import Connection
import pytz
# from sqlalchemy.orm import join


def run():
    #TODO event subscriber should be auto initialized with every command (use framework?)
    # CalendarEventSubscriber.get_instance()

    _to = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

    session = Connection.get_instance().get_session()
    signals = aliased(Signal)
    #TODO add some optional arg to fetch after some date
    # entries_to_update = session.query(CalendarEntry)\
    #     .outerjoin(signals, CalendarEntry.signals)\
    #     .filter(signals.id == None)\
    #     .filter(CalendarEntry.datetime <= _to)\
    #     .order_by(CalendarEntry.datetime.asc()).all()

    #TODO protect form duplicates

    # Run only if any news can be updated
    # if len(entries_to_update) is 0 or est_to_utc(entries_to_update[0].datetime) <= _to:
    #     scrapper = NewsScrapper()
    #     scrapper.run(entries_to_update[0].datetime)
    scrapper = NewsScrapper()
    scrapper.run(datetime.datetime.strptime('Jan 26 2018 01:00AM', '%b %d %Y %I:%M%p'), datetime.datetime.strptime('Jan 27 2018  11:00PM', '%b %d %Y %I:%M%p'), to_file=True)
    # #
    # test_entry = session.query(CalendarEntry).filter(CalendarEntry.id == 2405).first()
    # for test_entry in entries_to_update:
    #     LiveNewsSignalChecker.get_instance().check(test_entry)

def est_to_utc(_datetime):
    return _datetime.replace(tzinfo=pytz.timezone('US/Eastern')).astimezone(pytz.utc)


run()
