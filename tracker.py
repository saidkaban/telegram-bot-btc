import requests
from requests.api import get

def get_info():
    data = requests.get('https://dev-api.shrimpy.io/v1/exchanges/coinbasepro/candles?quoteTradingSymbol=USDT&baseTradingSymbol=BTC&interval=1H')
    candles = data.json()[-5:]
    candles = list(map(lambda obj: obj["high"], candles))
    maxValue = max(candles)
    message = "Son 5 saatteki en yüksek mum kapanışları\n\n{}\n{}\n{}\n{}\n{}\n\nEn yüksek kapanış: {}".format(candles[0],candles[1],candles[2],candles[3],candles[4],maxValue)
    return message


if __name__ == "__main__":
    print(get_info())