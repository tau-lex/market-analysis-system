# -*- coding: utf-8 -*-
import numpy as np


path = 'E:/Projects/market-analysis-system/data/crypto/'
files = ['BNBETH', 'BNBUSDT', 'BTCUSDT', 'ETHUSDT']#, 'BCCUSDT']

data = list()

for fn in files:
    for idx in range(11, 15):
        fname = '{path}{fn}/{nb}.csv'.format(path=path, fn=fn, nb=idx)
        data.append(np.genfromtxt(fname, delimiter=';', dtype=np.float))
        
    data = np.vstack(data)
    fname = '{path}{fn}{nb}.csv'.format(path=path, fn=fn, nb='03')
    np.savetxt(fname, data, fmt='%.8f', delimiter=';')
    data = list()
