import time
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
symbols = ['GBPCHF', 'GBPJPY', 'GBPUSD', 'NZDJPY', 'EURUSD', 'EURAUD']
tf = 240        # timeframe (period)
window = 20     # size history window (bar count)

# model
action = 'predict' # train1, train2, predict
wgt_path = 'E:/Projects/market-analysis-system/mas_vae/'
code = 60       # latent tensor size
filters = (3, 12) # convolution filters count
dropout = 0.4   # inside dropout

epochs = 10
batch = 128
img_width = window * 4
img_size = img_width * img_width * 3


#====== load data ======
# prefix = 'norm_w20'
filename = str(tf) + '_w' + str(window) + '.npz'
# create form
data = np.ones((img_size,), dtype=np.float)
data = np.reshape(data, (1, img_width, img_width, 3))

start_t = time.clock()
# load
for symbol in symbols:
    # compressed npz
    npz_file = np.load(dt_path + symbol + filename)
    new_data = npz_file.f.arr_0
    # csv data
    #new_data = np.genfromtxt(dt_path + prefix + symbol + filename, delimiter=';')
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

print('New data shape: {} \nRead+Calc time: {}'.format(x_train.shape, time.clock() - start_t))


#====== Train VAE ======
model_name = 'vae_img{}_flt{}-{}_code{}'.format(window, filters[0], filters[1], code)
encoder, decoder, autoencoder, _ = deep_conv2d_vae((img_width, img_width, 3),
                                    filters_count=filters,
                                    latent_dim=code,
                                    dropout=dropout)

# #====== create model ======
# from keras.models import Model
# from keras.layers import Input, Dense, concatenate, Lambda
# from keras.layers import Flatten, Reshape, BatchNormalization, Dropout
# from keras.layers import Conv2D, MaxPooling2D, Conv2DTranspose, UpSampling2D
# from keras.losses import mse, mae, mape
# from keras import backend as K

# def sampling(args):
#     z_mean, z_log_var = args
#     batch = K.shape(z_mean)[0]
#     dim = K.int_shape(z_mean)[1]
#     # by default, random_normal has mean=0 and std=1.0
#     epsilon = K.random_normal(shape=(batch, dim))
#     return z_mean + K.exp(0.5 * z_log_var) * epsilon

# input_shape = (img_width, img_width, 3)
# latent_dim = code
# filters_count = filters
# kernel_size = (3, 3)
# kernel_pooling = (2, 2)
# strides = (1, 1)
# initializer = 'truncated_normal'
    
# # Encoder
# input_tensor = Input(shape=input_shape, name='encoder_input')
# if len(input_shape) == 2:
#     x = Reshape((input_shape[0], input_shape[1], 1))(input_tensor)
# elif len(input_shape) == 3:
#     x = input_tensor
# x = Conv2D(filters=filters_count[0],
#             kernel_size=kernel_size,
#             padding='same',
#             activation='relu',
#             kernel_initializer=initializer,
#             strides=strides)(x)
# x = Dropout(dropout)(x)
# x = MaxPooling2D(kernel_pooling)(x)
# x = Conv2D(filters=filters_count[1],
#             kernel_size=kernel_size,
#             padding='same',
#             activation='relu',
#             kernel_initializer=initializer,
#             strides=strides)(x)
# x = Dropout(dropout)(x)
# x = MaxPooling2D(kernel_pooling)(x)
# # shape info needed to build decoder model
# shape = K.int_shape(x)
# # shape = enc.output_shape
# # generate latent vector Q(z|X)
# x = Flatten()(x)
# x = Dense(latent_dim*3, activation='relu', name='encoder_output')(x)

# z_mean = Dense(latent_dim, name='z_mean')(x)
# z_log_var = Dense(latent_dim, name='z_log_var')(x)
# # use reparameterization trick to push the sampling out as input
# # note that "output_shape" isn't necessary with the TensorFlow backend
# z = Lambda(sampling, output_shape=(latent_dim,), name='z')([z_mean, z_log_var])

# # Decoder
# latent_inputs = Input(shape=(latent_dim,), name='latent_input')
# y = Dense(shape[1] * shape[2] * shape[3], activation='relu')(latent_inputs)
# y = Reshape((shape[1], shape[2], shape[3]))(y)
# y = UpSampling2D(kernel_pooling)(y)
# y = Dropout(dropout)(y)
# y = Conv2DTranspose(filters=filters_count[1],
#                 kernel_size=kernel_size,
#                 padding='same',
#                 activation='relu',
#                 kernel_initializer=initializer,
#                 strides=strides)(y)
# y = UpSampling2D(kernel_pooling)(y)
# y = Dropout(dropout)(y)
# y = Conv2DTranspose(filters=filters_count[0],
#                 kernel_size=kernel_size,
#                 padding='same',
#                 activation='relu',
#                 kernel_initializer=initializer,
#                 strides=strides)(y)
# y = Conv2DTranspose(filters=(1 if len(input_shape) == 2 else 3),
#                 kernel_size=kernel_size,
#                 padding='same',
#                 activation='relu',
#                 kernel_initializer=initializer,
#                 strides=strides,
#                 name='decoder_output')(y)
# if len(input_shape) == 2:
#     output = Reshape((input_shape[0], input_shape[1]))(y)
# elif len(input_shape) == 3:
#     output = Reshape(input_shape)(y)

# # Create models
# encoder = Model(input_tensor, [z_mean, z_log_var, z], name='encoder')
# decoder = Model(latent_inputs, output, name='decoder')
# autoencoder = Model(input_tensor, decoder(encoder(input_tensor)[2]), name='ae')

# reconstruction_loss = mse(K.flatten(input_tensor), K.flatten(output))
# reconstruction_loss *= img_size
# kl_loss = 1 + z_log_var - K.square(z_mean) - K.exp(z_log_var)
# kl_loss = K.sum(kl_loss, axis=-1)
# kl_loss *= -0.5
# vae_loss = K.mean(reconstruction_loss + kl_loss)
# autoencoder.add_loss(vae_loss)
# autoencoder.compile(optimizer='rmsprop', metrics=['acc'])
# #==============

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
