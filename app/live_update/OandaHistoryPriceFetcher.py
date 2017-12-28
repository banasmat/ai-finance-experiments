from urllib.request import urlopen, Request
import xmltodict
from collections import OrderedDict
from app.model.PriceQuote import PriceQuote
from app.database.Connection import Connection
import datetime

from app.Config import Config
import sys
import json

from oandapyV20.contrib.factories import InstrumentsCandlesFactory
from oandapyV20 import API


class OandaHistoryPriceFetcher:

    def fetch(self, _from: datetime.datetime, _to: datetime.datetime, gran: str, symbol: str):

        instr = symbol[:3] + '_' + symbol[-3:]

        config = Config.get('oanda')
        client = API(access_token=config['api_key'])

        date_format_in = '%Y-%m-%dT%H:%M:%SZ'
        date_format_out = '%Y-%m-%dT%H:%M:%SZ'

        params = {
            "granularity": gran,
            "from": _from.strftime(date_format_in),
            "to": _to.strftime(date_format_in)
        }

        session = Connection.get_instance().get_session()

        for r in InstrumentsCandlesFactory(instrument=instr, params=params):
            print("REQUEST: {} {} {}".format(r, r.__class__.__name__, r.params))
            rv = client.request(r)

            for candle in r.response.get('candles'):
                dt = candle.get('time')[0:19]
                try:
                    if candle['complete']:
                        # TODO consider converting dt to GMT
                        quote = PriceQuote(symbol, dt, candle['mid']['h'], candle['mid']['l'], candle['volume'])
                        session.add(quote)

                except Exception as e:
                    print(e, r)

        session.commit()
