from app.live_update.LivePriceFetcher import LivePriceFetcher
import os
import datetime


def run():
    fetcher = LivePriceFetcher()

    try:
        fetcher.fetch()
    except Exception as e:
        with open(os.path.join(os.path.abspath(os.getcwd()), 'output', 'price-fetcher-errors.txt'),"a") as f:
            f.writelines('ERROR OCCURRED AT: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n' + str(e) + '\n\n')
        print(str(e))

# run()
