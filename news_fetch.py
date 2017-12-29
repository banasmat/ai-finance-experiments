from app.live_update.NewsScrapper import NewsScrapper
from app.live_update.LiveNewsSignalChecker import LiveNewsSignalChecker
import datetime
from app.event.CalendarEventSubscriber import CalendarEventSubscriber
from app.model.CalendarEntry import CalendarEntry
from app.database.Connection import Connection
import pytz

def run():
    #TODO event subscriber should be auto initialized with every command (use framework?)
    CalendarEventSubscriber.get_instance()

    session = Connection.get_instance().get_session()

    #TODO add some optional arg to fetch after some date
    entries_to_update = session.query(CalendarEntry)\
        .filter_by(actual='') \
        .order_by(CalendarEntry.datetime.asc()).all()


    print('calendar entries to update', len(entries_to_update))

    #TODO protect form duplicates

    # Run only if any news can be updated
    if len(entries_to_update) is 0 or est_to_utc(entries_to_update[0].datetime) <= datetime.datetime.utcnow().replace(tzinfo=pytz.utc):
        scrapper = NewsScrapper()
        scrapper.run(entries_to_update[0].datetime)
    # scrapper = NewsScrapper()
    # scrapper.run(datetime.datetime.strptime('Nov 28 2017  1:00AM', '%b %d %Y %I:%M%p'))

    # test_entry = session.query(CalendarEntry).filter(CalendarEntry.id == 123).first()
    # LiveNewsSignalChecker.get_instance().check(test_entry)

def est_to_utc(_datetime):
    return _datetime.replace(tzinfo=pytz.timezone('US/Eastern')).astimezone(pytz.utc)


run()
