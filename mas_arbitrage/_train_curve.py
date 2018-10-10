import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

from mas_tools.api import Binance


path = 'E:/Projects/market-analysis-system/mas_arbitrage/'

api = Binance('', '')

# 1m, 3m, 5m, 15m, 30m
# 1h, 2h, 4h, 6h, 8h
# 12h, 1d, 3d, 1w, 1M
period = '15m'
limit = 1000
base = 'BTCUSDT'
# pairs = ['ETHUSDT', 'BNBUSDT', 'BCCUSDT', 'EOSUSDT', 'ADAUSDT', 'LTCUSDT', 'NEOUSDT', 'XLMUSDT', 'XRPUSDT']
pairs = ['BCCUSDT']

symb1 = pd.DataFrame(
        api.candlesticks(symbol=base,
                interval=period, limit=limit),
        dtype=np.float)
x = symb1[4].values
# x = x.reshape((len(x)*4,))

symb2 = pd.DataFrame(
        api.candlesticks(symbol=pairs[0],
                interval=period, limit=limit),
        dtype=np.float)
y = symb2[4].values
# y = y.reshape((len(y)*4,))


from keras.models import Sequential
from keras.layers import Dense, BatchNormalization

model = Sequential()
model.add(Dense(32, activation='relu', input_shape=(1,)))
model.add(Dense(32, activation='elu'))
model.add(Dense(1, activation='linear'))
model.compile(optimizer='adam', loss='mse')

model.fit(x[100:900:2], y[100:900:2], epochs=10, shuffle=True)

plt.plot(x, y, 'o', label='Original data', markersize=1)
plt.plot(x, model.predict(x), 'r-', label='predicted data')

plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()
