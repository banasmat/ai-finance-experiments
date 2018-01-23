from sqlalchemy.exc import SQLAlchemyError
import os
from app.model.PriceQuote import PriceQuote
from app.database.Connection import Connection
import datetime
import pandas as pd

from app.Config import Config

from oandapyV20.contrib.factories import InstrumentsCandlesFactory
from oandapyV20 import API


class OandaHistoryPriceFetcher:
    config = Config.get('oanda')
    client = API(access_token=config['api_key'])

    date_format_in = '%Y-%m-%dT%H:%M:%SZ'
    date_format_out = '%Y-%m-%dT%H:%M:%S'

    def fetch_data_frame(self, _from: datetime.datetime, _to: datetime.datetime, gran: str, symbol: str):

        instr = symbol[:3] + '_' + symbol[-3:]

        params = {
            "granularity": gran,
            "from": _from.strftime(self.date_format_in),
            "to": _to.strftime(self.date_format_in)
        }

        candles = {}

        for r in InstrumentsCandlesFactory(instrument=instr, params=params):
            print("REQUEST: {} {} {}".format(r, r.__class__.__name__, r.params))
            self.client.request(r)
            for candle in r.response.get('candles'):
                dt = datetime.datetime.strptime(candle.get('time')[0:19], self.date_format_out)
                candles[dt] = []
                candles[dt].append(candle['mid']['o'])
                candles[dt].append(candle['mid']['h'])
                candles[dt].append(candle['mid']['l'])
                candles[dt].append(candle['mid']['c'])
                candles[dt].append(candle['volume'])

        df = pd.DataFrame.from_dict(candles, orient='index')
        df.columns = ['open', 'high', 'low', 'close', 'volume']

        return df

    def fetch_to_file(self, _from: datetime.datetime, _to: datetime.datetime, gran: str, symbol: str):
        file_path = os.path.join(os.path.abspath(os.getcwd()), 'resources', 'oanda_prices', symbol + '.csv')
        mode = 'w'
        if(os.path.isfile(file_path)):
            mode = 'a'
            with open(file_path, "r") as O:
                all_lines = O.readlines()
                last_line = all_lines[len(all_lines) - 1]
                last_dt = datetime.datetime.strptime(last_line[0:19], self.date_format_out)

                if gran == '1H':
                    delta = datetime.timedelta(hours=1)
                elif gran == '1D':
                    delta = datetime.timedelta(days=1)
                else:
                    delta = datetime.timedelta(minutes=1)

                _from = last_dt + delta

        instr = symbol[:3] + '_' + symbol[-3:]

        params = {
            "granularity": gran,
            "from": _from.strftime(self.date_format_in),
            "to": _to.strftime(self.date_format_in)
        }

        with open(file_path, mode) as O:

            for r in InstrumentsCandlesFactory(instrument=instr, params=params):
                print("REQUEST: {} {} {}".format(r, r.__class__.__name__, r.params))
                self.client.request(r)
                OandaHistoryPriceFetcher.__write_rec_to_file(r.response, O)

    @staticmethod
    def __write_rec_to_file(r, h):
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

    def fetch_to_db(self, _from: datetime.datetime, _to: datetime.datetime, gran: str, symbol: str):

        instr = symbol[:3] + '_' + symbol[-3:]

        params = {
            "granularity": gran,
            "from": _from.strftime(self.date_format_in),
            "to": _to.strftime(self.date_format_in)
        }

        session = Connection.get_instance().get_session()

        existing_quotes = session.query(PriceQuote) \
            .filter_by(symbol=symbol) \
            .filter(PriceQuote.datetime >= (_from - datetime.timedelta(minutes=1)))\
            .filter(PriceQuote.datetime <= _to).all()

        existing_quote_dts = list(map(lambda _quote: _quote.datetime.strftime(self.date_format_out), existing_quotes))

        try:
            for r in InstrumentsCandlesFactory(instrument=instr, params=params):
                print("REQUEST: {} {} {}".format(r, r.__class__.__name__, r.params))
                rv = self.client.request(r)

                for candle in r.response.get('candles'):
                    dt = candle.get('time')[0:19]
                    print(candle)
                    if candle['complete'] and dt not in existing_quote_dts:
                        quote = PriceQuote(symbol, datetime.datetime.strptime(dt, self.date_format_out), candle['mid']['h'], candle['mid']['l'], candle['volume'])
                        existing_quote_dts.append(dt)
                        session.add(quote)

            session.commit()

        except SQLAlchemyError as e:
            session.rollback()
            print(e)

        except Exception as e:
            print(e)
