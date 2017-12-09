from urllib.request import urlopen, Request
import xmltodict
import sqlalchemy


class LivePriceFetcher:
    fetch_url = "http://rates.fxcm.com/RatesXML"

    def fetch(self):
        req = Request(self.fetch_url, headers={'User-Agent': "Magic Browser"})
        file = urlopen(req)
        data = file.read()
        file.close()

        data = xmltodict.parse(data)
        print(data)


fetcher = LivePriceFetcher()
fetcher.fetch()
