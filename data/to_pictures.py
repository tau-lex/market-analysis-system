import os
import numpy as np

from mas_tools.data import timeseries_to_img

from files import FILES, PERIODS, CSV


print('Warning! Process may be very long.')
lpath = 'E:/Projects/market-analysis-system/data/transformed/'
spath = 'E:/Projects/market-analysis-system/data/pictured/'
window = 50
img_size = window*4 * window*4 * 3
count = 1000 # count images of last bars

if not os.path.exists(spath):
    os.makedirs(spath)

for symbol in FILES[:]:
    for tf in PERIODS[3:]:
        ## Load price history
        new_data = np.array([])
        data = np.genfromtxt(lpath+symbol+tf+CSV, delimiter=';')
        data = data[:, 1:5]
        ## Map range
        len_data = len(data) - window + 1
        if len_data < count:
            continue

        for idx in range(len_data-count, len_data):
            ## Get image from window in history
            image = timeseries_to_img(data[idx:idx+window])
            new_data = np.append(new_data, image)
            ## Print and save checkpoints
            if idx % 100 == 0: print('{} / {}'.format(idx, len_data))
            if idx % 500 == 0:
                np.savez_compressed(spath+symbol+tf+'_w'+str(window)+'.npz',
                                    new_data.reshape((idx+1-len_data-count, img_size)))
        ## Save image packet in to numpy archive
        new_data = new_data.reshape((count, img_size))
        print('{}{} : {}'.format(symbol, tf, new_data.shape))
        np.savez_compressed(spath+symbol+tf+'_w'+str(window)+'.npz', new_data)
        data = None
        new_data = None
