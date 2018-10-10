import numpy as np
from mas_tools.data import create_timeseries_matrix

from files import FILES, PERIODS, CSV

# lpath = 'E:/Projects/market-analysis-system/data/transformed/'
lpath = 'E:/Projects/market-analysis-system/data/normalized/'
spath = 'E:/Projects/market-analysis-system/data/windowed/'

window = 20 # warning! size of file multiply in to window size

for symbol in FILES:
    for tf in PERIODS:
    # tf = '1440'
        if tf == '1' or tf == '5' or tf =='15':
            continue
        data = np.genfromtxt(lpath+symbol+tf+CSV, delimiter=';')
        data, _ = create_timeseries_matrix(data, look_back=window)
        np.savetxt(spath+'norm_w_'+str(window)+symbol+tf+CSV, data, fmt='%0.6f', delimiter=';')
        data = []

