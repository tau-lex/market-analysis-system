# -*- coding: utf-8 -*-
import numpy as np


path = 'E:/Projects/market-analysis-system/data/crypto/'
files = ['BNBETH', 'BNBUSDT', 'BTCUSDT', 'ETHUSDT', 'BCCUSDT']
nb = '04'
data = None

for fn in files:
    fname = '{path}{name}{nb}.csv'.format(path=path, name=fn, nb=nb)
    newfname = '{path}{name}{nb}_candles.csv'.format(path=path, name=fn, nb=nb)
    data = np.genfromtxt(fname, delimiter=';', dtype=np.float)
    
    data = np.reshape(data, (len(data), 20, 15))
    data = data[:, :, 0:4]
    data = np.reshape(data, (len(data), 80))
    
    np.savetxt(newfname, data, fmt='%.8f', delimiter=';')
