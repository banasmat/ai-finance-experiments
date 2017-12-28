from app.live_update.OandaHistoryPriceFetcher import OandaHistoryPriceFetcher
from app.dataset.PreProcessedDataProvider import PreProcessedDataProvider
import os
import datetime


def run():
    from app.live_update.OandaHistoryPriceFetcher import OandaHistoryPriceFetcher
    import datetime

    fetcher = OandaHistoryPriceFetcher()

    _to = datetime.datetime.now(tz=datetime.timezone.utc)
    _from = _to - datetime.timedelta(days=1)

    currency_pairs = PreProcessedDataProvider.get_currency_pair_strings()

    for currency_pair in currency_pairs:
        try:
            fetcher.fetch(_from, _to, 'M1', currency_pair)
        except Exception as e:
            with open(os.path.join(os.path.abspath(os.getcwd()), 'output', 'price-fetcher-errors.txt'),"a") as f:
                f.writelines('ERROR OCCURRED AT: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n' + str(e) + '\n\n')
            print(str(e))


run()
