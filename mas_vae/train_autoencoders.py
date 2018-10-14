import random
import numpy as np

# OpenCL GPU accelerating
# http://github.com/plaidml
import plaidml.keras
plaidml.keras.install_backend()

from mas_tools.models.autoencoders import deep_conv2d_vae
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau

from sklearn.model_selection import train_test_split
from mas_tools.ml import plot_history
import matplotlib.pyplot as plt

# data
dt_path = 'E:/Projects/market-analysis-system/data/pictured/'
symbols = ['AUDJPY', 'AUDUSD', 'CHFJPY', 'EURAUD',
            'EURCAD', 'EURCHF', 'EURGBP', 'EURJPY',
            'EURRUB', 'EURUSD', 'GBPAUD', 'GBPCAD',
            'GBPCHF', 'GBPJPY', 'GBPUSD', 'NZDJPY',
            'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY',
            'USDRUB', 'XAGUSD', 'XAUUSD']
tf = 240        # timeframe (period)
window = 20     # size history window (bar count)

# model
action = 'train1' # train1, train2, predict
wgt_path = 'E:/Projects/market-analysis-system/mas_vae/'
code = 60       # latent tensor size
filters = (3, 12) # convolution filters count
dropout = 0.4   # inside dropout

epochs = 10
batch = 128
img_width = window * 4
img_size = img_width * img_width * 3


#====== load data ======
print('Load data...')
random.seed(666)
symbols = random.sample(symbols, 6)
filename = str(tf) + '_w' + str(window) + '.npz'
# create form
data = np.ones((img_size,), dtype=np.float)
data = np.reshape(data, (1, img_width, img_width, 3))
# load
for symbol in symbols:
    # compressed npz
    npz_file = np.load(dt_path + symbol + filename)
    new_data = npz_file.f.arr_0
    new_data = np.reshape(new_data, (len(new_data), img_width, img_width, 3))
    data = np.vstack((data, new_data))
# clean first row
data = data[1:]
x_train, x_test = train_test_split(data, shuffle=True, test_size=0.1)
# clear memory
data = None
# normalize imagess data
x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255

print('New data shape: {}'.format(x_train.shape))


#====== Build VAE ======
print('Build autoencoder...')
model_name = 'vae_img{}_flt{}-{}_code{}'.format(window, filters[0], filters[1], code)
encoder, decoder, autoencoder, vae_loss = deep_conv2d_vae((img_width, img_width, 3),
                                                            filters_count=filters,
                                                            latent_dim=code,
                                                            dropout=dropout)
# print(type(vae_loss))

autoencoder.compile(optimizer='rmsprop', loss='mse', metrics=['acc'])

if action in ['train2', 'predict']:
    autoencoder.load_weights(wgt_path + model_name + '.hdf5', by_name=True)
if action in ['train1', 'train2']:
    # reduce_lr = ReduceLROnPlateau(factor=0.1, patience=3, min_lr=0.00001, verbose=1)
    
    history = autoencoder.fit(x_train, x_train,
                            epochs=epochs,
                            batch_size=batch,
                            shuffle=True,
                            # callbacks=[reduce_lr],
                            validation_data=(x_test, x_test))

    autoencoder.save_weights(wgt_path + model_name + '.hdf5')
    encoder.save_weights(wgt_path + model_name + '_enc.hdf5')
    # decoder.save_weights(wgt_path + model_name + '_dec.hdf5')
    plot_history(history, acc='acc')
    print('Weight saved.')


#====== View ======
n = 10
test_z_mean, test_z_log_var, test_z = encoder.predict(x_test, batch_size=batch)

if action == 'predict':
    # display a histogram of the digit classes in the latent space
    filename = wgt_path + model_name + '_latent-distr.png'
    for idx in range(n*n):
        plt.hist(test_z[idx], bins=50)
    plt.xlabel('z size')
    plt.savefig(filename)
    plt.close()

    filename = wgt_path + model_name + '_latent-distr-mean.png'
    for idx in range(n*n):
        plt.hist(test_z_mean[idx], bins=50)
    plt.xlabel('z size')
    plt.savefig(filename)
    plt.close()

    filename = wgt_path + model_name + '_latent-distr--log.png'
    for idx in range(n*n):
        plt.hist(test_z_log_var[idx], bins=50)
    plt.xlabel('z size')
    plt.savefig(filename)
    plt.close()

if action == 'train1' or action == 'train2':
    ## Origin test data
    figure = np.zeros((img_width * n, img_width * n, 3))
    _test = x_test[:100]
    for idx in range(10):
        for jdx in range(10):
            digit = _test[idx*10+jdx].reshape(img_width, img_width, 3)
            figure[idx * img_width: (idx + 1) * img_width,
                    jdx * img_width: (jdx + 1) * img_width] = digit

    filename = wgt_path + model_name + '_origin_pics.png'
    fig = plt.figure()
    img = plt.imshow(figure) 
    plt.colorbar(img)
    plt.title('origin 100 examples')
    plt.savefig(filename)
    plt.close()

    ## Decoded test data
    figure = np.zeros((img_width * n, img_width * n, 3))
    z_sample = test_z_mean[:100, :]
    x_decoded = decoder.predict(z_sample)
    for idx in range(10):
        for jdx in range(10):
            digit = x_decoded[idx*10+jdx].reshape(img_width, img_width, 3)
            figure[idx * img_width: (idx + 1) * img_width,
                    jdx * img_width: (jdx + 1) * img_width] = digit * 100

    filename = wgt_path + model_name + '_restored_from_z__mean.png'
    fig = plt.figure()
    img = plt.imshow(figure) 
    plt.colorbar(img)
    plt.title('z mean 100 examples')
    plt.savefig(filename)
    plt.close()

    figure = np.zeros((img_width * n, img_width * n, 3))
    z_sample = test_z_log_var[:100, :]
    x_decoded = decoder.predict(z_sample)
    for idx in range(10):
        for jdx in range(10):
            digit = x_decoded[idx*10+jdx].reshape(img_width, img_width, 3)
            figure[idx * img_width: (idx + 1) * img_width,
                    jdx * img_width: (jdx + 1) * img_width] = digit * 100

    filename = wgt_path + model_name + '_restored_from_z_log.png'
    fig = plt.figure()
    img = plt.imshow(figure) 
    plt.colorbar(img)
    plt.title('z log 100 examples')
    plt.savefig(filename)
    plt.close()

    figure = np.zeros((img_width * n, img_width * n, 3))
    z_sample = test_z[:100, :]
    x_decoded = decoder.predict(z_sample)
    for idx in range(10):
        for jdx in range(10):
            digit = x_decoded[idx*10+jdx].reshape(img_width, img_width, 3)
            figure[idx * img_width: (idx + 1) * img_width,
                    jdx * img_width: (jdx + 1) * img_width] = digit * 100

    filename = wgt_path + model_name + '_restored_from_z.png'
    fig = plt.figure()
    img = plt.imshow(figure) 
    plt.colorbar(img)
    plt.title('z 100 examples')
    plt.savefig(filename)
    plt.close()
