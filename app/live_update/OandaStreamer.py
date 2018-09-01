import json
from oandapyV20 import API
from oandapyV20.exceptions import V20Error
from oandapyV20.endpoints.pricing import PricingStream
from app.Config import Config


class OandaStreamer(object):

    @staticmethod
    def fetch():
        access_token = Config.get('oanda')['api_key']
        account_id = Config.get('oanda')['account_id']

        api = API(access_token=access_token, environment="practice")

        instruments = "DE30_EUR,EUR_USD,EUR_JPY"
        s = PricingStream(accountID=account_id, params={"instruments": instruments})
        try:
            n = 0
            for R in api.request(s):
                print(json.dumps(R, indent=2))
                n += 1
                if n > 10:
                    s.terminate("maxrecs received: {}".format(MAXREC))

        except V20Error as e:
            print("Error: {}".format(e))

