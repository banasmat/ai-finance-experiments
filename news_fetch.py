from app.live_update.NewsScrapper import NewsScrapper
import datetime

scrapper = NewsScrapper()
scrapper.run()
# scrapper.run(datetime.datetime.today() - datetime.timedelta(days=1))