from app.live_update.NewsScrapper import NewsScrapper
from app.live_update.LiveNewsSignalChecker import LiveNewsSignalChecker
import datetime
from app.event.CalendarEventSubscriber import CalendarEventSubscriber
from app.model.CalendarEntry import CalendarEntry
from app.database.Connection import Connection


def run():
    #TODO event subscriber should be auto initialized with every command (use framework?)
    CalendarEventSubscriber.get_instance()

    session = Connection.get_instance().get_session()

    entries_to_update = session.query(CalendarEntry)\
        .filter_by(actual='').all()

    # Run only if any news can be updated
    if len(entries_to_update) is 0 or entries_to_update[0].datetime <= datetime.datetime.now():
        scrapper = NewsScrapper()
        scrapper.run()
        # scrapper.run(datetime.datetime.today() - datetime.timedelta(days=1))


    # test_entry = session.query(CalendarEntry).filter(CalendarEntry.title != '').first()
    # LiveNewsSignalChecker.get_instance().check(test_entry)

# run()
