import zope.event
import zope.event.classhandler
from app.event.CalendarEntryUpdatedEvent import CalendarEntryUpdatedEvent
from app.live_update.LiveNewsSignalChecker import LiveNewsSignalChecker
from app.live_update.LiveNewsSignalChecker import LiveNewsSignalChecker


class CalendarEventSubscriber(object):

    __instance = None

    signal_checker = LiveNewsSignalChecker()

    @staticmethod
    def get_instance():
        """ Static access method. """
        if CalendarEventSubscriber.__instance is None:
            CalendarEventSubscriber()
        return CalendarEventSubscriber.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if CalendarEventSubscriber.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CalendarEventSubscriber.__instance = self
            self.__set_up()

    def __set_up(self):
        zope.event.classhandler.handler(CalendarEntryUpdatedEvent, self.on_calendar_entry_updated)

    def on_calendar_entry_updated(self, event):
        self.signal_checker.check(event.calendar_entry)

