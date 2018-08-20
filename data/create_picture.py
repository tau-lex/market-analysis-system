import time
import numpy as np
import matplotlib.pyplot as plt

from mas_tools.data import timeseries_to_img

plt.style.use('dark_background')

lpath = 'E:/Projects/market-analysis-system/data/transformed/'
spath = 'E:/Projects/market-analysis-system/data/'
fn = 'GBPUSD240'
window = 50

new_data = np.genfromtxt(lpath+fn+'.csv', delimiter=';')

data = new_data[800:920, 1:5]

# plt.plot(data[:, 0])
# plt.plot(data[:, 1])
# plt.plot(data[:, 2])
# plt.plot(data[:, 3])
# plt.legend(['open', 'high', 'low', 'close'])
# plt.savefig(spath + fn + '_plt.png')
# plt.close()
# # plt.show()

imgs = np.array([])

for idx in range(800, 900):
    image = timeseries_to_img(new_data[idx:idx+window, 1:5])
    image.save(spath + 'test/' + fn + '_pil_' + str(idx) + '.png', 'PNG')
    imgs = np.append(imgs, image)

imgs = imgs.reshape((100, window*4, window*4, 3))
print(imgs.shape)
print(imgs[2, :, :, 1])
print(imgs.dtype)

# imgs = imgs.reshape((100, (window*4+1) * (window*4+1) * 3))
# np.savetxt(spath + 'test/_numpy_array.csv', imgs,
#             delimiter=';', fmt='%.0f')
# np.savez_compressed(spath + 'test/_numpy_array.npz', imgs)

# print('Saved\nNow read and save as image')

# loaded_imgs = np.load(spath + 'test/_numpy_array.npz')
# print(loaded_imgs.f.arr_0.shape)

# from PIL import Image
# pic = np.reshape(imgs[99], (window*4+1, window*4+1, 3)).astype(np.float)
# pic = Image.fromarray(pic)
# pic.show()
