import json

from oandapyV20.contrib.requests import MarketOrderRequest, TakeProfitDetails, StopLossDetails
import oandapyV20.endpoints.orders as orders
import oandapyV20

from app.Config import Config


class OandaTrader(object):

    @staticmethod
    def place_order(currency_pair, stop_loss, take_profit):

        currency_pair = currency_pair[:3] + '_' + currency_pair[-3:]

        access_token = Config.get('oanda')['api_key']

        api = oandapyV20.API(access_token=access_token)

        mkt_order = MarketOrderRequest(
            instrument=currency_pair,
            units=1,
            takeProfitOnFill=TakeProfitDetails(price=take_profit).data,
            stopLossOnFill=StopLossDetails(price=stop_loss).data)

        # create the OrderCreate request
        r = orders.OrderCreate(access_token, data=mkt_order.data)
        try:
            # create the OrderCreate request
            rv = api.request(r)
        except oandapyV20.exceptions.V20Error as err:
            print(r.status_code, err)
        else:
            print(json.dumps(rv, indent=2))
