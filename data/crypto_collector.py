import time
import requests
from threading import Thread

import numpy as np
import pandas as pd

from mas_tools.api import Binance

api = Binance('', '')
symbols = ['BTCUSDT', 'ETHUSDT', 'BNBETH', 'BNBUSDT']
period = '1m'

limit = 20
ticks = 0
save_period = 1000
path = 'd:/mas/'

data = dict(zip(symbols, [dict({'data':[]}) for i in symbols]))


while True:
    try:
        start_time = time.time()
        for symbol in symbols:
            candles = pd.DataFrame(api.candlesticks(symbol=symbol, interval=period, limit=limit), dtype=np.float)
            tickers = pd.DataFrame(api.tickers(symbol=symbol, limit=limit))
            trades = pd.DataFrame(api.aggr_trades(symbol=symbol, limit=limit), dtype=np.float)
            # data[symbol]['candles'] = np.column_stack((candles.values[:, 1:6], # o,h,l,c,v
            #                                                     candles.values[:, 7:11])) # qav, nt, bv, qv
            # data[symbol]['tickers'] = np.column_stack(([np.array([x[0:2] for x in tickers['bids'].values], dtype=np.float),
            #                                                     np.array([x[0:2] for x in tickers['asks'].values], dtype=np.float)]))
            # data[symbol]['trades'] = trades[['p', 'q']].values
            data[symbol]['data'] = np.append(data[symbol]['data'], np.column_stack((np.column_stack((candles.values[:, 1:6], # o,h,l,c,v
                                                                                                     candles.values[:, 7:11])), # qav, nt, bv, qv
                                                                                    np.column_stack(([np.array([x[0:2] for x in tickers['bids'].values], dtype=np.float),
                                                                                                      np.array([x[0:2] for x in tickers['asks'].values], dtype=np.float)])),
                                                                                    trades[['p', 'q']].values))).reshape(len(data[symbol]['data'])+1, limit*15)

        if ticks % save_period == 0:
            for symbol in symbols:
                fname = path + symbol + '/' + str(round(time.time())) + '.csv'
                np.savetxt(fname, data[symbol]['data'], delimiter=';', fmt='%.8f')
                print('{} saved.'.format(fname))
                data[symbol]['data'] = np.array([])

        ticks += 1
        # print('tick. {} s.'.format(time.time()-start_time))
        time.sleep(5)

    except requests.exceptions.ConnectionError as e:
        print(e)
        
    except TimeoutError as e:
        print('TimeoutError:', e)
        
    # except Exception as e:
    #     print('Error:', e)
    #     break

    except KeyboardInterrupt:
        print('Exit...')
        for symbol in symbols:
                fname = path + symbol + '/' + str(round(time.time())) + '.csv'
                np.savetxt(fname, data[symbol]['data'], delimiter=';', fmt='%.8f')
                data[symbol]['data'] = np.array([])
                print('{} saved.'.format(fname))
        break


# def get_candles(symbol):
#     while True:
#         try:
#             candles = pd.DataFrame(api.candlesticks(symbol=symbol, interval=period, limit=limit), dtype=np.float)
#             data[symbol]['candles'] = np.column_stack((candles.values[:, 1:6], # o,h,l,c,v
#                                                     candles.values[:, 7:11])) # qav, nt, bv, qv
#         except Exception as e:
#             print('get_candles:', e)
#         except KeyboardInterrupt:
#             print('Exit...')
#             break
#         time.sleep(.5)

# def get_tickers(symbol):
#     while True:
#         try:
#             tickers = pd.DataFrame(api.tickers(symbol=symbol, limit=limit))
#             data[symbol]['tickers'] = np.column_stack(([np.array([x[0:2] for x in tickers['bids'].values], dtype=np.float),
#                                                         np.array([x[0:2] for x in tickers['asks'].values], dtype=np.float)]))
#         except Exception as e:
#             print('get_tickers:', e)
#         except KeyboardInterrupt:
#             print('Exit...')
#             break
#         time.sleep(.5)

# def get_trades(symbol):
#     while True:
#         try:
#             trades = pd.DataFrame(api.aggr_trades(symbol=symbol, limit=limit), dtype=np.float)
#             data[symbol]['trades'] = trades[['p', 'q']].values
#         except Exception as e:
#             print('get_trades:', e)
#         except KeyboardInterrupt:
#             print('Exit...')
#             break
#         time.sleep(.5)

# def saver():
#     ticks = 1
#     while True:
#         try:
#             start_time = time.time()
#             if ticks % save_period == 0:
#                 print('Save...')
#                 for symbol in symbols:
#                     np.savetxt(path+symbol+'.csv', np.column_stack((data[symbol]['candles'],
#                                                                     data[symbol]['tickers'],
#                                                                     data[symbol]['trades'])), delimiter=';', fmt='%.8f')

#             ticks += 1
#             time.sleep(1.0)
#             print('tick. {} s.'.format(time.time()-start_time))

# # Подготавливаем потоки, складываем их в массив
# threads = []
# for symbol in symbols:
#     threads.append(Thread(target=get_candles, args=(symbol,)))
#     threads.append(Thread(target=get_tickers, args=(symbol,)))
#     threads.append(Thread(target=get_trades, args=(symbol,)))
# threads.append(Thread(target=saver))

# # Запускаем каждый поток
# for thread in threads:
#     if not thread.is_alive():
#         thread.start()

# # Ждем завершения каждого потока
# for thread in threads:
#     thread.join()

