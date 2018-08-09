from keras import backend as K
from keras.models import Model, Sequential
from keras.layers import Input, Dense, concatenate
from keras.layers import Flatten, Reshape, BatchNormalization
from keras.layers import Conv2D, MaxPooling2D, Conv2DTranspose

from mas_tools.ml import save_model_arch


def deep_conv2d_ae(input_shape):

    latent_dim = 32
    kernel_size = (1, 5)
    kernel_pooling = (1, 2)
    strides = (1, 1)
    
    # Encoder
    input_tensor = Input(shape=input_shape, name='encoder_input')
    x = Conv2D(filters=32,
                kernel_size=kernel_size,
                padding='same',
                activation='relu',
                strides=strides,
                input_shape=input_shape)(input_tensor)
    x = Conv2D(filters=64,
                kernel_size=kernel_size,
                padding='same',
                activation='relu',
                strides=strides)(x)
    # shape info needed to build decoder model
    shape = K.int_shape(x)
    # shape = enc.output_shape
    # generate latent vector Q(z|X)
    x = Flatten()(x)
    x = Dense(latent_dim, activation='relu', name='encoder_output')(x)

    # Decoder
    latent_inputs = Input(shape=(latent_dim,), name='latent_input')
    y = Dense(shape[1] * shape[2] * shape[3], activation='relu')(latent_inputs)
    y = Reshape((shape[1], shape[2], shape[3]))(y)
    y = Conv2DTranspose(filters=64,
                    kernel_size=kernel_size,
                    padding='same',
                    activation='relu',
                    strides=strides)(y)
    y = Conv2DTranspose(filters=32,
                    kernel_size=kernel_size,
                    padding='same',
                    activation='relu',
                    strides=strides)(y)
    y = Conv2DTranspose(filters=1,
                    kernel_size=kernel_size,
                    padding='same',
                    activation='relu',
                    strides=strides,
                    name='decoder_output')(y)

    # Create models
    encoder = Model(input_tensor, x, name='encoder')
    decoder = Model(latent_inputs, y, name='decoder')
    autoencoder = Model(input_tensor, decoder(encoder(input_tensor)), name='ae')

    return encoder, decoder, autoencoder


if __name__ == "__main__":
    path = 'E:/Projects/market-analysis-system/'

    enc, dec, ae = deep_conv2d_ae((4, 20, 1))
    save_model_arch(enc, path+'ae_enc')
    enc.summary()
    save_model_arch(dec, path+'ae_dec')
    dec.summary()
    save_model_arch(ae, path+'ae')
    ae.summary()
    