# https://gist.github.com/pohzipohzi/ad7942fc5545675022c1f31123e64c0c

from bs4 import BeautifulSoup
import requests
import datetime
import logging
import csv
import os
from app.model.CalendarEntry import CalendarEntry
from app.database.Connection import Connection
from app.event.CalendarEntryUpdatedEvent import CalendarEntryUpdatedEvent
import zope.event


class NewsScrapper(object):

    def run(self, start_date: datetime.datetime=None, end_date: datetime.datetime=None):

        if start_date is None:
            start_date = datetime.datetime.now().replace(hour=0, minute=0, second=0)
        if end_date is None:
            end_date = datetime.datetime.now().replace(hour=0, minute=0, second=0)

        delta = end_date - start_date
        mod = delta.days % 7
        if mod != 0:
            end_date = end_date + datetime.timedelta(days=(7-mod))

        path_base = 'calendar.php?week='
        # Dec11.2017
        dt_format = '%b%d.%Y'
        # self.setLogger()

        self.getEconomicCalendar(path_base + start_date.strftime(dt_format).lower(), path_base + end_date.strftime(dt_format).lower())

    def setLogger(self):
        logs_path = os.path.join(os.path.abspath(os.getcwd()), 'output', 'news_scrapper_logs')
        logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename=logs_path,
                        filemode='w')
        console = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

    def getEconomicCalendar(self, startlink ,endlink):
        session = Connection.get_instance().get_session()

        print(startlink)

        # write to console current status
        logging.info("Scraping data for link: {}".format(startlink))

        # get the page and make the soup
        baseURL = "https://www.forexfactory.com/"
        r = requests.get(baseURL + startlink)
        data = r.text
        soup = BeautifulSoup(data, "lxml")

        # get and parse table data, ignoring details and graph
        table = soup.find("table", class_="calendar__table")

        # do not use the ".calendar__row--grey" css selector (reserved for historical data)
        trs = table.select("tr.calendar__row.calendar_row")
        fields = ["date","time","currency","impact","event","actual","forecast","previous"]

        # some rows do not have a date (cells merged)
        curr_year = startlink[-4:]
        curr_date = ""
        curr_time = ""
        for tr in trs:

            # fields may mess up sometimes, see Tue Sep 25 2:45AM French Consumer Spending
            # in that case we append to errors.csv the date time where the error is
            try:
                for field in fields:
                    data = tr.select("td.calendar__cell.calendar__{}.{}".format(field,field))[0]
                    # print(data)
                    if field=="date" and data.text.strip()!="":
                        curr_date = data.text.strip()
                    elif field=="time" and data.text.strip()!="":
                        # time is sometimes "All Day" or "Day X" (eg. WEF Annual Meetings)
                        if data.text.strip().find("Day")!=-1:
                            curr_time = "12:00am"
                        else:
                            curr_time = data.text.strip()
                    elif field=="currency":
                        currency = data.text.strip()
                    elif field=="impact":
                        # when impact says "Non-Economic" on mouseover, the relevant
                        # class name is "Holiday", thus we do not use the classname
                        impact = data.find("span")["title"]
                    elif field=="event":
                        event = data.text.strip()
                    elif field=="actual":
                        actual = data.text.strip()
                    elif field=="forecast":
                        forecast = data.text.strip()
                    elif field=="previous":
                        previous = data.text.strip()

                dt = datetime.datetime.strptime(",".join([curr_year,curr_date,curr_time]),
                                                "%Y,%a%b %d,%I:%M%p")

                #TODO save only news that have titles konwn by nn

                #TODO give option to save to csv (if dumping ALL news for training)

                calendar_entry = session.query(CalendarEntry).filter_by(currency=currency, datetime=dt, title=event).first()

                if calendar_entry is None and previous != '':
                    calendar_entry = CalendarEntry(currency, dt, event, actual, forecast, previous)
                    session.add(calendar_entry)
                elif actual != '' and len(calendar_entry.signals) == 0:
                    calendar_entry.actual = actual
                    calendar_entry.updated_at = datetime.datetime.now()
                    calendar_event = CalendarEntryUpdatedEvent(calendar_entry)
                    zope.event.notify(calendar_event)

            except Exception as e:
                with open(os.path.join(os.path.abspath(os.getcwd()), 'output', 'news-scrapper-errors.csv'),"a") as f:
                    csv.writer(f).writerow([curr_year,curr_date,curr_time, str(e)])

        session.commit()

        # exit recursion when last available link has reached
        if startlink == endlink:
            logging.info("Successfully retrieved data")
            return

        # get the link for the next week and follow
        follow = soup.select("a.calendar__pagination.calendar__pagination--next.next")
        follow = follow[0]["href"]
        self.getEconomicCalendar(follow, endlink)
