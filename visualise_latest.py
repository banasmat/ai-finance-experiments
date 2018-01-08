import datetime
from app.model.CalendarEntry import CalendarEntry
from app.model.PriceQuote import PriceQuote
from app.model.Signal import Signal
from app.database.Connection import Connection
from app.dataset.DataSetProvider import DataSetProvider
from app.dataset.DataVisualizer import DataVisualizer
from sqlalchemy import or_

def run():

    data_set_provider = DataSetProvider()
    data_visualizer = DataVisualizer()

    currency_pair = 'EURUSD'
    # currency_pair = 'EURCAD'
    # currency_pair = 'AUDJPY'

    curr_1 = currency_pair[:3]
    curr_2 = currency_pair[-3:]

    session = Connection.get_instance().get_session()

    now = datetime.datetime.now()

    date_from = now - datetime.timedelta(days=385)
    date_to = now - datetime.timedelta(days=365)

    entries_and_signals = session.query(CalendarEntry, Signal) \
        .join(CalendarEntry.signals)\
        .filter(Signal.symbol == currency_pair)\
        .filter(CalendarEntry.datetime >= date_from)\
        .filter(CalendarEntry.datetime <= date_to) \
        .filter(or_(CalendarEntry.currency == curr_1, CalendarEntry.currency == curr_2))\
        .all()

    entries_to_show = list(map(lambda x: x[0], entries_and_signals))
    signals_to_show = list(map(lambda x: x[1], entries_and_signals))

    prices_to_show = session.query(PriceQuote) \
        .filter(PriceQuote.datetime >= date_from)\
        .filter(PriceQuote.datetime <= date_to)\
        .filter(PriceQuote.symbol == currency_pair)\
        .all()

    prices, news = data_set_provider.data_frames_from_records(entries_to_show, prices_to_show, currency_pair)

    # prices = prices.fillna(0)

    labels = list(map(lambda signal: signal.value, signals_to_show))

    data_visualizer.visualize(prices, news, labels, currency_pair + '_latest')


run()
