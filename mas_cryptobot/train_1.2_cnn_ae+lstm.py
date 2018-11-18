#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import numpy as np

# # OpenCL GPU accelerating
# # http://github.com/plaidml
import plaidml.keras
plaidml.keras.install_backend()

from mas_tools.models.autoencoders import deep_conv2d_vae
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau

from keras.models import Model
from keras.layers import Input, LSTM, Dense, Reshape

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
wgt_path1 = 'E:/Projects/market-analysis-system/mas_vae/'
wgt_path2 = 'E:/Projects/market-analysis-system/mas_cryptobot/'
code = 60       # latent tensor size
filters = (3, 12) # convolution filters count
dropout = 0.4   # inside dropout
lstm_size = 64

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
# normalize images data
data = data.astype('float32') / 255

print('Data shape: {}'.format(data.shape))


#====== Build encoder ======
print('Build encoder layers...')
model_name = 'vae_img{}_flt{}-{}_code{}_enc'.format(window, filters[0], filters[1], code)
encoder, _, _, _ = deep_conv2d_vae((img_width, img_width, 3),
                                    filters_count=filters,
                                    latent_dim=code,
                                    dropout=dropout)

encoder.compile(optimizer='rmsprop', loss='mse')
encoder.load_weights(wgt_path1 + model_name + '.hdf5', by_name=True)
encoder.trainable = False

# generate output
_, _, y_data = encoder.predict(data, batch_size=batch)
data = data[:-1]
y_data = y_data[1:]
x_train, x_test, y_train, y_test = train_test_split(data, y_data, shuffle=False, test_size=0.1)
# clear memory
data = None
y_data = None

#====== Build lstm ======
print('Build lstm layers...')
model_name = 'istm_conv{}-{}-{}-{}_lstm{}'.format(window, filters[0], filters[1], code, lstm_size)
picture_tensor = Input(shape=(img_width, img_width, 3), name='encoder_input')

input_tensor = Input(shape=(code,), name='lstm_input')
lstm = Reshape((1, code))(input_tensor)
lstm = LSTM(lstm_size, return_sequences=True)(lstm)
lstm = LSTM(lstm_size)(lstm)
lstm = Dense(code, activation='linear')(lstm)

lstm = Model(input_tensor, lstm, name='lstm_layers')
model = Model(picture_tensor, lstm(encoder(picture_tensor)[2]), name='conv-lstm_layers')

model.compile(optimizer='rmsprop', loss='mse', metrics=['acc'])

if action in ['train2', 'predict']:
    model.load_weights(wgt_path2 + model_name + '.hdf5', by_name=True)
if action in ['train1', 'train2']:
    reduce_lr = ReduceLROnPlateau(factor=0.1, patience=3, min_lr=0.00001, verbose=1)
    
    history = model.fit(x_train, y_train,
                        epochs=epochs,
                        batch_size=batch,
                        shuffle=False,
                        callbacks=[reduce_lr],
                        validation_data=(x_test, y_test))

    model.save_weights(wgt_path2 + model_name + '.hdf5')
    plot_history(history, acc='acc')
    print('Weight saved.')

