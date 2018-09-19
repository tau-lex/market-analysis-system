import os
import matplotlib.pyplot as plt

from keras import backend as K
from keras.models import Model, Sequential
from keras.layers import Input, Dense, concatenate, Lambda
from keras.layers import Flatten, Reshape, BatchNormalization, Dropout
from keras.layers import Conv2D, MaxPooling2D, Conv2DTranspose, UpSampling2D
from keras.losses import mse, mae, mape, binary_crossentropy
from keras import backend as K

from mas_tools.ml import save_model_arch


# reparameterization trick
# instead of sampling from Q(z|X), sample eps = N(0,I)
# then z = z_mean + sqrt(var)*eps
def sampling(args):
    """Reparameterization trick by sampling fr an isotropic unit Gaussian.
    Arguments
        args (tensor): mean and log of variance of Q(z|X)
    Returns
        z (tensor): sampled latent vector
    """

    z_mean, z_log_var = args
    batch = K.shape(z_mean)[0]
    dim = K.int_shape(z_mean)[1]
    # by default, random_normal has mean=0 and std=1.0
    epsilon = K.random_normal(shape=(batch, dim))
    return z_mean + K.exp(0.5 * z_log_var) * epsilon


def deep_conv2d_vae(input_shape,
                    latent_dim = 160):
    """"""
    kernel_size = (3, 3)
    kernel_pooling = (2, 2)
    strides = (1, 1)
    dropout = 0.5
    initializer = 'truncated_normal'
    
    # Encoder
    input_tensor = Input(shape=input_shape, name='encoder_input')
    if len(input_shape) == 2:
        x = Reshape((input_shape[0], input_shape[1], 1))(input_tensor)
    elif len(input_shape) == 3:
        x = input_tensor
    # x = BatchNormalization()(x)
    x = Conv2D(filters=32,
                kernel_size=kernel_size,
                padding='same',
                activation='relu',
                kernel_initializer=initializer,
                strides=strides)(x)
    x = Dropout(dropout)(x)
    x = MaxPooling2D(kernel_pooling)(x)
    x = Conv2D(filters=64,
                kernel_size=kernel_size,
                padding='same',
                activation='relu',
                kernel_initializer=initializer,
                strides=strides)(x)
    x = Dropout(dropout)(x)
    x = MaxPooling2D(kernel_pooling)(x)
    # shape info needed to build decoder model
    shape = K.int_shape(x)
    # shape = enc.output_shape
    # generate latent vector Q(z|X)
    x = Flatten()(x)
    x = Dense(100, activation='relu', name='encoder_output')(x)

    z_mean = Dense(latent_dim, name='z_mean')(x)
    z_log_var = Dense(latent_dim, name='z_log_var')(x)
    # use reparameterization trick to push the sampling out as input
    # note that "output_shape" isn't necessary with the TensorFlow backend
    z = Lambda(sampling, output_shape=(latent_dim,), name='z')([z_mean, z_log_var])

    # Decoder
    latent_inputs = Input(shape=(latent_dim,), name='latent_input')
    y = Dense(shape[1] * shape[2] * shape[3], activation='relu')(latent_inputs)
    y = Reshape((shape[1], shape[2], shape[3]))(y)
    y = UpSampling2D(kernel_pooling)(y)
    y = Dropout(dropout)(y)
    y = Conv2DTranspose(filters=64,
                    kernel_size=kernel_size,
                    padding='same',
                    activation='relu',
                    kernel_initializer=initializer,
                    strides=strides)(y)
    y = UpSampling2D(kernel_pooling)(y)
    y = Dropout(dropout)(y)
    y = Conv2DTranspose(filters=32,
                    kernel_size=kernel_size,
                    padding='same',
                    activation='relu',
                    kernel_initializer=initializer,
                    strides=strides)(y)
    y = Conv2DTranspose(filters=(1 if len(input_shape) == 2 else 3),
                    kernel_size=kernel_size,
                    padding='same',
                    activation='relu',
                    kernel_initializer=initializer,
                    strides=strides,
                    name='decoder_output')(y)
    # y = BatchNormalization()(y)
    if len(input_shape) == 2:
        output = Reshape((input_shape[0], input_shape[1]))(y)
    elif len(input_shape) == 3:
        output = Reshape(input_shape)(y)

    # Create models
    encoder = Model(input_tensor, [z_mean, z_log_var, z], name='encoder')
    decoder = Model(latent_inputs, output, name='decoder')
    autoencoder = Model(input_tensor, decoder(encoder(input_tensor)[2]), name='ae')

    reconstruction_loss = mse(K.flatten(input_tensor), K.flatten(output))
    if len(input_shape) == 2:
        reconstruction_loss *= (input_shape[0] * input_shape[1])
    elif len(input_shape) == 3:
        reconstruction_loss *= (input_shape[0] * input_shape[1] * input_shape[2])
    kl_loss = 1 + z_log_var - K.square(z_mean) - K.exp(z_log_var)
    kl_loss = K.sum(kl_loss, axis=-1)
    kl_loss *= -0.5
    vae_loss = K.mean(reconstruction_loss + kl_loss)
    # autoencoder.add_loss(vae_loss)
    # autoencoder.compile(optimizer='adam', metrics=['acc'])

    return encoder, decoder, autoencoder, vae_loss


if __name__ == "__main__":
    path = 'E:/Projects/market-analysis-system/'

    enc, dec, ae, _ = deep_conv2d_vae((80, 80, 3))
    save_model_arch(enc, path+'ae_enc')
    enc.summary()
    save_model_arch(dec, path+'ae_dec')
    dec.summary()
    save_model_arch(ae, path+'ae')
    ae.summary()
