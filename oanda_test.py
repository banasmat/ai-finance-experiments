import oandapy
from app.Config import Config

config = Config.get('oanda')

oanda = oandapy.API(environment="practice", access_token=config['api_key'])

response = oanda.get_prices(instruments="EUR_USD")
prices = response.get("prices")
asking_price = prices[0].get("ask")

print(prices)