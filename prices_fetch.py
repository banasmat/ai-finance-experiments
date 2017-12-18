from app.live_update.LivePriceFetcher import LivePriceFetcher


def run():
    fetcher = LivePriceFetcher()
    fetcher.fetch()

# run()
