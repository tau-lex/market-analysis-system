# -*- coding: utf-8 -*-
import numpy as np


path = 'E:/Projects/market-analysis-system/data/crypto/'
files = ['BNBETH', 'BNBUSDT', 'BTCUSDT', 'ETHUSDT', 'BCCUSDT']
nb = '04'
data = None

for fn in files:
    fname = '{path}{name}{nb}.csv'.format(path=path, name=fn, nb=nb)
    newfname = '{path}{name}{nb}_candles+tickers.csv'.format(path=path, name=fn, nb=nb)
    data = np.genfromtxt(fname, delimiter=';', dtype=np.float)
    
    data = np.reshape(data, (len(data), 20, 15))

    data_p = data[:, :, 0:4]
    data_p = np.reshape(data_p, (len(data), 80))
    data_t = data[:, :, 10:14]
    data_t = np.reshape(data_t, (len(data), 80))

    data = np.hstack((data_p, data_t))
    
    np.savetxt(newfname, data, fmt='%.8f', delimiter=';')
