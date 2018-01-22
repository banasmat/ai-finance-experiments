from app.live_update.OandaHistoryPriceFetcher import OandaHistoryPriceFetcher
from app.dataset.PreProcessedDataProvider import PreProcessedDataProvider
import os
import datetime
from app.database.Connection import Connection
from app.model.PriceQuote import PriceQuote


def run():

    fetcher = OandaHistoryPriceFetcher()

    _to = datetime.datetime.now(tz=datetime.timezone.utc)
    _from = _to - datetime.timedelta(hours=120)

    # currency_pairs = PreProcessedDataProvider.get_currency_pair_strings()
    currency_pairs = ['EURUSD']

    for currency_pair in currency_pairs:
        try:
            fetcher.fetch(_from, _to, 'H1', currency_pair)
        except Exception as e:
            with open(os.path.join(os.path.abspath(os.getcwd()), 'output', 'price-fetcher-errors.txt'),"a") as f:
                f.writelines('ERROR OCCURRED AT: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n' + str(e) + '\n\n')
            print(str(e))


        session = Connection.get_instance().get_session()

        existing_quotes = session.query(PriceQuote) \
            .filter_by(symbol=currency_pair) \
            .filter(PriceQuote.datetime >= (_from - datetime.timedelta(minutes=1))) \
            .filter(PriceQuote.datetime <= _to).all()

# run()