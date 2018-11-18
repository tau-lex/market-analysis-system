#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import numpy as np

# OpenCL GPU accelerating
# http://github.com/plaidml
import plaidml.keras
plaidml.keras.install_backend()

from mas_tools.models.autoencoders import deep_conv2d_vae
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, TensorBoard

from mas_tools.ml import plot_history
import matplotlib.pyplot as plt


random.seed(666)

## Data
# 1
dt_path = 'E:/Projects/market-analysis-system/data/pictured/'
symbols = [
    'AUDJPY', 'AUDUSD', 'CHFJPY', 'EURAUD',
    'EURCAD', 'EURCHF', 'EURGBP', 'EURJPY',
    'EURRUB', 'EURUSD', 'GBPAUD', 'GBPCAD',
    'GBPCHF', 'GBPJPY', 'GBPUSD', 'NZDJPY',
    'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY',
    'USDRUB', 'XAGUSD', 'XAUUSD'
]
tfs = [
    '1', '5', '15', '30',
    '60', '240', '1440'
]
tf = 240        # timeframe (period)
window = 20     # size history window (bar count)
# .. from random files
rnd = random.sample
filenames = ['{}{}_w{}.npz'.format(symbol, rnd(tfs, 1)[0], window) for symbol in rnd(symbols, 6)]
# # 2
# dt_path = 'E:/Projects/market-analysis-system/data/crypto/'
# symbols = [
#     'BCCUSDT', 'BNBETH', 'BNBUSDT',
#     'BTCUSDT', 'ETHUSDT'
# ]
# postfix = '{n}_candles.csv'
# window = 20     # size history window (bar count)


## Model
wgt_path = 'E:/Projects/market-analysis-system/mas_cryptobot/wgts/'
# Select mode:
# Training from scratch - train1, 
# Training a trained model - train2,
# Predicting - predict
action = 'train1'
# latent tensor size
code = 60
# convolution filters count
filters = (4, 12)
# inside dropout
dropout = 0.5

model_name = 'vae_w{}_flt{}-{}_code{}'.format(window, filters[0], filters[1], code)
epochs = 10
batch = 128
# image sizes
img_width = window * 4
img_size = img_width * img_width * 3


## Load data
print('Load data...')
# Create form
x_data = np.ones((img_size,), dtype=np.float)
x_data = np.reshape(x_data, (1, img_width, img_width, 3))
# Load
for filename in filenames:
    # compressed npz
    npz_file = np.load(dt_path + filename)
    new_data = npz_file.f.arr_0
    new_data = np.reshape(new_data, (len(new_data), img_width, img_width, 3))
    x_data = np.vstack((x_data, new_data))
# clean first row
x_data = x_data[1:]
# normalize imagess data
x_data = x_data.astype('float32') / 255
print('New data shape:', x_data.shape)


## Build VAE
print('Build autoencoder...')
encoder, decoder, autoencoder, vae_loss = deep_conv2d_vae((img_width, img_width, 3),
                                                            filters_count=filters,
                                                            latent_dim=code,
                                                            dropout=dropout)
# TODO How to use vae_loss?
# print(type(vae_loss))
autoencoder.compile(optimizer='rmsprop', loss='mse', metrics=['acc'])


## Train or do prediction
if action in ['train2', 'predict']:
    autoencoder.load_weights(wgt_path + model_name + '.hdf5', by_name=True)
if action in ['train1', 'train2']:
    print('Train model...')
    # reduce_lr = ReduceLROnPlateau(factor=0.1, patience=3, min_lr=0.00001, verbose=1)
    # chpt = ModelCheckpoint(wgt_path + model_name + '_{}.hdf5')
    # tb = TensorBoard()
    
    # Train
    history = autoencoder.fit(
        x_data, x_data,
        epochs=epochs,
        batch_size=batch,
        validation_split=0.1,
        shuffle=True,
        # callbacks=[tb]
    )

    # Save weights
    autoencoder.save_weights(wgt_path + model_name + '.hdf5')
    encoder.save_weights(wgt_path + model_name + '_enc.hdf5')
    plot_history(history, acc='acc')


## Visual evaluation
# Number of examples = n^2
n = 10
test_z_mean, test_z_log_var, test_z = encoder.predict(x_data[-100:], batch_size=batch)

# Save images of origin and decoded data
if action in ['train1', 'train2', 'predict']:
    def plot_data(fname, plot_data):
        figure = np.zeros((img_width * n, img_width * n, 3))
        plot_data = plot_data[-(n*n):]
        for idx in range(n):
            for jdx in range(n):
                digit = plot_data[idx*n+jdx].reshape(img_width, img_width, 3)
                figure[(idx * img_width): ((idx + 1) * img_width),
                        (jdx * img_width): ((jdx + 1) * img_width)] = digit

        fig = plt.figure()
        img = plt.imshow(figure) 
        plt.colorbar(img)
        plt.savefig(fname)
        plt.close()

    # Origin test data
    plot_data(wgt_path+model_name+'_origin_pics.png', x_data)
    # Decoded test data
    plot_data(wgt_path+model_name+'_restored_from_z_1.png', decoder.predict(test_z[:100, :]))
    # plot_data(wgt_path+model_name+'_restored_from_z_mean.png', decoder.predict(test_z_mean[:100, :]))
    # plot_data(wgt_path+model_name+'_restored_from_z_log.png', decoder.predict(test_z_log_var[:100, :]))

# Save a histogram of the digit classes in the latent space
if action in ['train2']:
    def plot_hist(fname, hist_data):
        for idx in range(n):
            plt.hist(hist_data[idx], bins=100)
        plt.xlabel('z size')
        plt.savefig(fname)
        plt.close()
    
    plot_hist(wgt_path+model_name+'_latent-distr.png', test_z)
    # plot_hist(wgt_path+model_name+'_latent-distr-mean.png', test_z_mean)
    # plot_hist(wgt_path+model_name+'_latent-distr--log.png', test_z_log_var)
