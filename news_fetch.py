from app.live_update.NewsScrapper import NewsScrapper
import datetime
from app.event.CalendarEventSubscriber import CalendarEventSubscriber


#TODO event subscriber should be auto initialized with every command
CalendarEventSubscriber.get_instance()

scrapper = NewsScrapper()
scrapper.run()
# scrapper.run(datetime.datetime.today() - datetime.timedelta(days=1))
