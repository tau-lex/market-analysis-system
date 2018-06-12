from mas_tools.api import Binance

import pandas as pd

MY_API_KEY = '---'
MY_API_SECRET = '---'

bot = Binance(API_KEY=MY_API_KEY, API_SECRET=MY_API_SECRET)

# print(bot.ping())
# {}

# print(bot.server_time())
# {'serverTime': 1528312118494}

# print(bot.exchange_info())
# {
#     "timezone": "UTC",
#     "serverTime": 1508631584636,
#     "rateLimits": [{
#         "rateLimitType": "REQUESTS",
#         "interval": "MINUTE",
#         "limit": 1200
#     }, {
#         "rateLimitType": "ORDERS",
#         "interval": "SECOND",
#         "limit": 10
#     }, {
#         "rateLimitType": "ORDERS",
#         "interval": "DAY",
#         "limit": 100000
#     }],
#     "exchangeFilters": [],
#     "symbols": [{
#         "symbol": "ETHBTC",
#         "status": "TRADING",
#         "baseAsset": "ETH",
#         "baseAssetPrecision": 8,
#         "quoteAsset": "BTC",
#         "quotePrecision": 8,
#         "orderTypes": ["LIMIT", "MARKET"],
#         "icebergAllowed": False,
#         "filters": [{
#             "filterType": "PRICE_FILTER",
#             "minPrice": "0.00000100",
#             "maxPrice": "100000.00000000",
#             "tickSize": "0.00000100"
#         }, {
#             "filterType": "LOT_SIZE",
#             "minQty": "0.00100000",
#             "maxQty": "100000.00000000",
#             "stepSize": "0.00100000"
#         }, {
#             "filterType": "MIN_NOTIONAL",
#             "minNotional": "0.00100000"
#         }]
#     }]
# }

# History candlesticks
# data = pd.DataFrame(bot.candlesticks(symbol='ETHUSDT', interval='1h', limit=5),
#                     columns=['time','open','high','low','close','volume','close time',
#                     'quote volume','nb trades','base volume','quote volume','ignore'])
# print(data)
# indexes: [0] = now() - limit; [limit-1] = current candle
#             time          open          high           low         close          volume     close time      quote volume  nb trades     base volume      quote volume ignore
# 0  1528635600000  564.64000000  571.18000000  560.23000000  569.90000000   4354.46766000  1528639199999  2465370.82302600       3756   2440.39093000  1383556.73798860      0
# 1  1528639200000  569.90000000  570.43000000  565.15000000  566.50000000   1544.62761000  1528642799999   877686.13160500       2040    740.98554000   421140.59755400      0
# 2  1528642800000  566.50000000  568.45000000  564.58000000  567.44000000   2606.89482000  1528646399999  1476366.83814600       2122   1189.46030000   673848.54584130      0
# 3  1528646400000  567.08000000  567.50000000  561.79000000  561.79000000   2773.05404000  1528649999999  1563806.66222970       2506   1461.30690000   824057.70556360      0
# 4  1528650000000  561.79000000  562.93000000  538.39000000  540.00000000  17274.84863000  1528653599999  9497987.27212920      10819  10363.43909000  5701933.52655430      0

# Current best tickers
# print(bot.tickers(symbol='ETHUSDT', limit=5))
# {
#     'lastUpdateId': 7676363,
#     'bids': [
#         ['0.68300000', '28158.51000000', []],
#         ['0.68290000', '2508.78000000', []],
#         ['0.68230000', '611.15000000', []],
#         ['0.68229000', '52.76000000', []],
#         ['0.68197000', '73.28000000', []]
#     ],
#     'asks': [
#         ['0.68301000', '52.85000000', []],
#         ['0.68308000', '52.85000000', []],
#         ['0.68316000', '52.85000000', []],
#         ['0.68321000', '74.21000000', []],
#         ['0.68322000', '52.84000000', []]
#     ]
# }

# # Day stats
# print(bot.ticker_24(symbol='ETHUSDT'))

# # Current ask price
# print(bot.ticker_price(symbol='ETHUSDT'))
# {
#     'symbol': 'ETHUSDT',
#     'price': '569.65000000'
# }

# # Current ticker: bid/ask prices and qty's
# print(bot.ticker_book_price(symbol='ETHUSDT'))
# {
#     'symbol': 'ETHUSDT',
#     'bidPrice': '568.87000000',
#     'bidQty': '0.00013000',
#     'askPrice': '569.00000000',
#     'askQty': '1.07667000'
# }

# Closed trades
# print(bot.trades(symbol='ETHUSDT', limit=5))
# [{
#     'id': 27906843,
#     'price': '522.38000000',
#     'qty': '0.79100000',
#     'time': 1528811416344,
#     'isBuyerMaker': False, # была ли покупка по указанной покупателем цене, 
#     'isBestMatch': True # была ли встречная сделка
# }]

# History trades
# print(bot.h_trades(symbol='ETHUSDT', limit=5))
# [{
#     "id": 28457,
#     "price": "4.00000100",
#     "qty": "12.00000000",
#     "time": 1499865549590,
#     "isBuyerMaker": true,
#     "isBestMatch": true
# }]

# History aggregate trades
# print(bot.aggr_trades(symbol='ETHUSDT', limit=5))
# [{
#     'a': 24806414,      # tradeId строки
#     'p': '522.51000000',# Цена
#     'q': '0.03273000',  # Количество
#     'f': 27906950,      # Первая tradeId
#     'l': 27906950,      # Последняя tradeId
#     'T': 1528811526591, # Время
#     'm': False,         # Was the buyer the maker?
#     'M': True           # Was the trade the best price match?
# }]

# PRIVATE METHODS
import time

local_time = int(time.time())
limits = bot.exchange_info()
server_time = int(limits['serverTime'])//1000

shift_seconds = server_time-local_time
bot.set_shift_seconds(shift_seconds)

# print(bot.account())
# {
#     "makerCommission": 15,
#     "takerCommission": 15,
#     "buyerCommission": 0,
#     "sellerCommission": 0,
#     "canTrade": true,
#     "canWithdraw": true,
#     "canDeposit": true,
#     "updateTime": 123456789,
#     "balances": [{
#         "asset": "BTC",
#         "free": "4723846.89208129",
#         "locked": "0.00000000"
#     }, {
#         "asset": "LTC",
#         "free": "4763368.68006011",
#         "locked": "0.00000000"
#     }]
# }

# print(bot.new_order(symbol='ETHUSDT'))

# print(bot.ticker_book_price(symbol='ETHUSDT'))

# print(bot.ticker_book_price(symbol='ETHUSDT'))