import schedule
import time

# import news_fetch
# import prices_fetch
from app.dataset.XBRLDataSetProvider import XBRLDataSetProvider


schedule.every(6).hours.do(XBRLDataSetProvider.gather_stock_prices())

# TODO consider fetching prices only during trading hours (for sure do not fetch on weekends)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)

while True:
    XBRLDataSetProvider.gather_stock_prices()
    schedule.run_pending()
    time.sleep(5 * 60 * 60)