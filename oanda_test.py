from app.live_update.OandaHistoryPriceFetcher import OandaHistoryPriceFetcher
import datetime

fetcher = OandaHistoryPriceFetcher()
#
# _to = datetime.datetime.now()
# _from = _to - datetime.timedelta(days=2)


_to = datetime.datetime.strptime('Sep 29 2017  1:00AM', '%b %d %Y %I:%M%p')
_from = _to - datetime.timedelta(days=20)


fetcher.fetch(_from, _to, 'M1', 'EURUSD')
