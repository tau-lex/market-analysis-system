import os
import numpy as np

from mas_tools.data import timeseries_to_img

from files import FILES, PERIODS, CSV


lpath = 'E:/Projects/market-analysis-system/data/transformed/'
spath = 'E:/Projects/market-analysis-system/data/pictured/'
window = 20
img_size = (window*4+1) * (window*4+1) * 3
count = 1000 # count images of last bars

if not os.path.exists(spath):
    os.makedirs(spath)

for symbol in FILES[19:]:
    for tf in PERIODS:
    # tf = '1440'
    # symbol = 'AUDUSD'
    # tfdir = spath + symbol + tf + '_' + str(window) + '/'
    # if not os.path.exists(tfdir):
    #     os.makedirs(tfdir)
        new_data = np.array([])
        data = np.genfromtxt(lpath+symbol+tf+CSV, delimiter=';')
        data = data[:, 1:5]
        len_data = len(data) - window + 1
        if len_data < count:
            continue

        for idx in range(len_data-count, len_data):
            image = timeseries_to_img(data[idx:idx+window])
            # image.save(tfdir + '{:5d}'.format(idx) + '.png', 'PNG')
            new_data = np.append(new_data, image)
            
            if idx % 100 == 0: print('{} / {}'.format(idx, len_data))
            if idx % 500 == 0:
                np.savez_compressed(spath+symbol+tf+'_w'+str(window)+'.npz',
                                    new_data.reshape((idx+1-len_data-count, img_size)))
        #-for
        new_data = new_data.reshape((count, img_size))
        print('{}{} : {}'.format(symbol, tf, new_data.shape))
        np.savez_compressed(spath+symbol+tf+'_w'+str(window)+'.npz', new_data)
        data = None
        new_data = None

