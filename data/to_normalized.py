import numpy as np

from files import FILES, PERIODS, CSV


print('Warning! Process may be very long.')
lpath = 'E:/Projects/market-analysis-system/data/transformed/'
spath = 'E:/Projects/market-analysis-system/data/normalized/'

for symbol in FILES:
    for tf in PERIODS:
        ## Read
        data = np.genfromtxt(lpath+symbol+tf+CSV, delimiter=';')[:, 1:5]
        ## Normalize
        data /= max(np.max(data[:, 0]), np.max(data[:, 1]), np.max(data[:, 2]), np.max(data[:, 3]))
        ## Save
        np.savetxt(spath+symbol+tf+CSV, data, fmt='%0.6f', delimiter=';')
        data = None
