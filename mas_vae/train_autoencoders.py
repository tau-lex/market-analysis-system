import time
import numpy as np
import matplotlib.pyplot as plt

# import mas_tools.models.autoencoders as vae
from models import deep_conv2d_vae

from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau

from sklearn.model_selection import train_test_split
from mas_tools.ml import plot_history

wpath = 'E:/Projects/market-analysis-system/mas_vae/'
lpath = 'E:/Projects/market-analysis-system/data/pictured/'

symbols = ['GBPCHF', 'GBPJPY', 'GBPUSD', 'NZDJPY', 'EURUSD']
window = 20
# prefix = 'norm_w20'
tf = '240_w20.npz'
# tf = '1_w20.npz'
model_name = 'conv_vae_' + str(window) + '_'
batch = 128
img_width = window * 4
img_size = window*4 * window*4 * 3


#====== load data ======
data = np.ones((img_size,), dtype=np.float)
data = np.reshape(data, (1, img_width, img_width, 3))

start_t = time.clock()
for symbol in symbols:
    npz_file = np.load(lpath + symbol + tf)
    new_data = npz_file.f.arr_0
    # new_data = np.genfromtxt(lpath+prefix+symbol+tf, delimiter=';')
    new_data = np.reshape(new_data, (len(new_data), img_width, img_width, 3))
    data = np.vstack((data, new_data))
data = data[1:]
x_train, x_test = train_test_split(data, shuffle=True, test_size=0.1)
data = None # Clear memory
x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255

print('New data shape: {} \nRead+Calc time: {}'.format(x_train.shape, time.clock()-start_t))


#====== Train AE ======
encoder, decoder, autoencoder, _ = deep_conv2d_vae((img_width, img_width, 3))

autoencoder.compile(optimizer='rmsprop', loss='mse', metrics=['acc'])

action = 'train1'
if action in ['train2', 'predict']:
    autoencoder.load_weights(wpath+model_name+'_ended.hdf5', by_name=True)
if action in ['train1', 'train2']:
    # reduce_lr = ReduceLROnPlateau(factor=0.1, patience=3, min_lr=0.00001, verbose=1)
    
    history = autoencoder.fit(x_train, x_train,
                            epochs=3,
                            batch_size=batch,
                            shuffle=True,
                            # callbacks=[reduce_lr],
                            validation_data=(x_test, x_test))

    autoencoder.save_weights(wpath+model_name+'_ended.hdf5')
    plot_history(history, acc='acc')


#====== View ======
filename = wpath + model_name + "vae_mean.png"
# display a 2D plot of the digit classes in the latent space
z_mean, _, _ = encoder.predict(x_test, batch_size=batch)
for idx in range(100):
    plt.plot(z_mean[idx])
plt.xlabel("latent space index")
plt.ylabel("z size")
plt.savefig(filename)
plt.show()

filename = wpath + model_name + "origin_pics.png"
n = 10
digit_size = window * 4
figure = np.zeros((digit_size * n, digit_size * n, 3))

_test = x_test[:100]
for idx in range(10):
    for jdx in range(10):
        digit = _test[idx*10+jdx].reshape(digit_size, digit_size, 3)
        figure[idx * digit_size: (idx + 1) * digit_size,
                jdx * digit_size: (jdx + 1) * digit_size] = digit

fig = plt.figure()
img = plt.imshow(figure) 
plt.colorbar(img)
plt.title('100 examples')
plt.savefig(filename)
plt.show()

filename = wpath + model_name + "pics_over_latent.png"
figure = np.zeros((digit_size * n, digit_size * n, 3))
z_sample = z_mean[:100, :]
x_decoded = decoder.predict(z_sample)
for idx in range(10):
    for jdx in range(10):
        digit = x_decoded[idx*10+jdx].reshape(digit_size, digit_size, 3)
        figure[idx * digit_size: (idx + 1) * digit_size,
                jdx * digit_size: (jdx + 1) * digit_size] = digit # * 255

fig = plt.figure()
img = plt.imshow(figure) 
plt.colorbar(img)
plt.title('100 examples')
plt.savefig(filename)
plt.show()


