import numpy as np

# from sklearn.preprocessing import scale
# X = scale( X, axis=0, with_mean=True, with_std=True, copy=True )

from files import FILES, PERIODS, CSV

lpath = 'E:/Projects/market-analysis-system/data/transformed/'
spath = 'E:/Projects/market-analysis-system/data/normalized/'

for symbol in FILES:
    for tf in PERIODS:
        data = np.genfromtxt(lpath+symbol+tf+CSV, delimiter=';')
        data = data[:, 1:5]
        dmax = max(np.max(data[:, 0]), np.max(data[:, 1]), np.max(data[:, 2]), np.max(data[:, 3]))
        data /= dmax
        np.savetxt(spath+symbol+tf+CSV, data, fmt='%0.6f', delimiter=';')
        data = []

