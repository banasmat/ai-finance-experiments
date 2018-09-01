from urllib.request import urlopen, Request
import xmltodict
from collections import OrderedDict
from app.model.PriceQuote import PriceQuote
from app.database.Connection import Connection
import datetime
from dateutil import tz


class LivePriceFetcher:

    def fetch(self):

        session = Connection.get_instance().get_session()

        req = Request("http://rates.fxcm.com/RatesXML", headers={'User-Agent': "Magic Browser"})
        file = urlopen(req)
        data = file.read()
        file.close()

        data = xmltodict.parse(data)
        rates: OrderedDict = data.get('Rates').get('Rate')

        # TODO probably shouldn't save if last quote datetime hasn't changed

        for rate in rates:
            symbol = rate.get('@Symbol')
            #TODO get from saved list of trained symbols
            if len(symbol) == 6:
                dt = datetime.datetime.now()
                time = datetime.datetime.strptime(rate.get('Last'), '%H:%M:%S')

                # For now we're saving in local timezone TODO does it make a difference?
                # timezone = tz.gettz('America/New_York')
                # dt.replace(tzinfo=timezone)
                # time = time.replace(tzinfo=timezone)

                dt = dt.replace(hour=time.hour, minute=time.minute, second=time.second)
                quote = PriceQuote(symbol, dt, rate.get('High'), rate.get('Low'))

                session.add(quote)

        session.commit()
