from app.live_update.OandaHistoryPriceFetcher import OandaHistoryPriceFetcher
import datetime
from app.dataset.PreProcessedDataProvider import PreProcessedDataProvider
from app.live_update.OandaStreamer import OandaStreamer


fetcher = OandaHistoryPriceFetcher()
#
# _to = datetime.datetime.now()
# _from = datetime.datetime.strptime('Jan 1 2001  1:00AM', '%b %d %Y %I:%M%p')
#
#
# _to = datetime.datetime.strptime('Jan 1 2001  1:00AM', '%b %d %Y %I:%M%p')
# _from = _to - datetime.timedelta(days=1)
#
# pp = PreProcessedDataProvider()
#
# for sym in pp.get_currency_pairs():
#     symbol = sym[0] + sym[1]
#     if symbol == 'EURUSD':
#         continue
#     fetcher.fetch(_from, _to, 'H1', symbol, to_file=True)
OandaStreamer.fetch()