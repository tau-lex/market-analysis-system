import numpy as np

# from sklearn.preprocessing import scale
# X = scale( X, axis=0, with_mean=True, with_std=True, copy=True )

from files import FILES, PERIODS, CSV

lpath = 'E:/Projects/market-analysis-system/data/transformed/'
spath = 'E:/Projects/market-analysis-system/data/normalized/'

for symbol in FILES:
    for tf in PERIODS:
        # tf = '240'
        data = np.genfromtxt(lpath+symbol+tf+CSV, delimiter=';')
        data = data[:, 1:5]
        data /= np.max(np.abs(data), axis=0)
        np.savetxt(spath+symbol+tf+CSV, data, fmt='%0.6f', delimiter=';')
        data = []

