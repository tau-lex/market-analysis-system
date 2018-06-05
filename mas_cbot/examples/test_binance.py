import time

from mas_tools.api import Binance

MY_API_KEY = '---'
MY_API_SECRET = '---'

bot = Binance(API_KEY = MY_API_KEY, API_SECRET = MY_API_SECRET)

# print(bot.ping())
# time.sleep(1)

# print(bot.time())
# time.sleep(1)

# 
print(bot.exchange_info(symbol='XRPUSDT'))
time.sleep(1)


# # Closed orders
# print(bot.trades(symbol='XRPUSDT', limit=500))
# time.sleep(1)

#
# print(bot.historicalTrades(symbol='XRPUSDT'))
# time.sleep(1)

# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# # Candlesticks
# data = pd.DataFrame(bot.candlesticks(symbol='XRPUSDT', interval='1h', limit=100))
# # print(data)
# plt.plot(data[4].apply(pd.to_numeric).values)
# plt.show()
# # time.sleep(1)

# # Tickers
# print(bot.tickers(symbol='XRPUSDT', limit=100))
# time.sleep(1)

# # Day stats
# print(bot.ticker24hr(symbol='XRPUSDT'))
# time.sleep(1)

# # Current ask price
# print(bot.tickerPrice(symbol='XRPUSDT'))
# time.sleep(1)

# # Current ticker: bid/ask prices and qty's
# print(bot.tickerBookTicker(symbol='XRPUSDT'))
# time.sleep(1)


