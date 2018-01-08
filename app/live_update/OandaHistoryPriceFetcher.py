from sqlalchemy.exc import SQLAlchemyError
import os
from app.model.PriceQuote import PriceQuote
from app.database.Connection import Connection
import datetime

from app.Config import Config

from oandapyV20.contrib.factories import InstrumentsCandlesFactory
from oandapyV20 import API


class OandaHistoryPriceFetcher:

    def fetch(self, _from: datetime.datetime, _to: datetime.datetime, gran: str, symbol: str, to_file=False):

        instr = symbol[:3] + '_' + symbol[-3:]

        config = Config.get('oanda')
        client = API(access_token=config['api_key'])

        date_format_in = '%Y-%m-%dT%H:%M:%SZ'
        date_format_out = '%Y-%m-%dT%H:%M:%S'


        params = {
            "granularity": gran,
            "from": _from.strftime(date_format_in),
            "to": _to.strftime(date_format_in)
        }

        if to_file:
            with open(os.path.join(os.path.abspath(os.getcwd()), 'resources', 'oanda_prices', symbol + '.csv'), "w") as O:
                for r in InstrumentsCandlesFactory(instrument=instr, params=params):
                    print("REQUEST: {} {} {}".format(r, r.__class__.__name__, r.params))
                    rv = client.request(r)
                    OandaHistoryPriceFetcher.cnv(r.response, O)
            return

        session = Connection.get_instance().get_session()

        existing_quotes = session.query(PriceQuote) \
            .filter_by(symbol=symbol) \
            .filter(PriceQuote.datetime >= (_from - datetime.timedelta(minutes=1)))\
            .filter(PriceQuote.datetime <= _to).all()

        existing_quote_dts = list(map(lambda _quote: _quote.datetime.strftime(date_format_out), existing_quotes))

        try:
            for r in InstrumentsCandlesFactory(instrument=instr, params=params):
                print("REQUEST: {} {} {}".format(r, r.__class__.__name__, r.params))
                rv = client.request(r)

                for candle in r.response.get('candles'):
                    dt = candle.get('time')[0:19]
                    print(candle)
                    if candle['complete'] and dt not in existing_quote_dts:
                        quote = PriceQuote(symbol, datetime.datetime.strptime(dt, date_format_out), candle['mid']['h'], candle['mid']['l'], candle['volume'])
                        existing_quote_dts.append(dt)
                        session.add(quote)

            session.commit()

        except SQLAlchemyError as e:
            session.rollback()
            print(e)

        except Exception as e:
            print(e)

    @staticmethod
    def cnv(r, h):
        for candle in r.get('candles'):
            ctime = candle.get('time')[0:19]
            try:
                rec = "{time},{complete},{o},{h},{l},{c},{v}".format(
                    time=ctime,
                    complete=candle['complete'],
                    o=candle['mid']['o'],
                    h=candle['mid']['h'],
                    l=candle['mid']['l'],
                    c=candle['mid']['c'],
                    v=candle['volume'],
                )
            except Exception as e:
                print(e, r)
            else:
                h.write(rec + "\n")
