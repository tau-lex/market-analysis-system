from keras.models import Model
from keras.layers import Input, Dense, concatenate
from keras.layers import Flatten, Reshape, BatchNormalization
from keras.layers import Conv2D, Conv2DTranspose, MaxPooling2D, UpSampling2D
from keras.regularizers import L1L2


def create_dense_ae(input_shape, encoding_dim=64, output_activation='linear'):
    """
    Example from https://habr.com/post/331382/

    Arguments
        input_shape (tuple of int):
        encoding_dim (int):
        output_activation (str):

    Returns
        encoder:
        decoder:
        autoencoder:
    """

    decoder_dim = 1
    for i in input_shape:
        decoder_dim *= i

    # Encoder
    input_tensor = Input(shape=input_shape)
    x = Flatten()(input_tensor)
    encoded = Dense(encoding_dim,
            activation='relu',
            kernel_initializer='glorot_uniform')(x)
    
    # Decoder
    input_encoded = Input(shape=(encoding_dim,))
    y = Dense(decoder_dim,
            activation=output_activation,
            kernel_initializer='glorot_uniform')(input_encoded)
    decoded = Reshape(input_shape)(y)

    # Create models
    encoder = Model(input_tensor, encoded, name="encoder")
    decoder = Model(input_encoded, decoded, name="decoder")
    autoencoder = Model(input_tensor, decoder(encoder(input_tensor)), name="autoencoder")

    return encoder, decoder, autoencoder


def create_deep_ae(input_shape, encoding_dim=64,
                    output_activation='linear', kernel_activation='elu',
                    lambda_l1=0.0):
    """
    Example from https://habr.com/post/331382/

    Arguments
        input_shape (tuple of int):
        encoding_dim (int):
        output_activation (str):
        kernel_activation (str):
        lambda_l1 (float): Regularisation value for sparse encoding.

    Returns
        encoder:
        decoder:
        autoencoder:
    """

    decoder_dim = 1
    for i in input_shape:
        decoder_dim *= i

    # Encoder
    input_tensor = Input(shape=input_shape)
    x = Flatten()(input_tensor)
    # x = Dense(encoding_dim*4, activation=kernel_activation)(x)
    x = Dense(encoding_dim*3, activation=kernel_activation)(x)
    x = Dense(encoding_dim*2, activation=kernel_activation)(x)
    encoded = Dense(encoding_dim, activation='linear',
                    activity_regularizer=L1L2(lambda_l1, 0))(x)
    
    # Decoder
    input_encoded = Input(shape=(encoding_dim,))
    y = Dense(encoding_dim*2, activation=kernel_activation)(input_encoded)
    y = Dense(encoding_dim*3, activation=kernel_activation)(y)
    # y = Dense(encoding_dim*4, activation=kernel_activation)(y)
    y = Dense(decoder_dim, activation=output_activation)(y)
    decoded = Reshape(input_shape)(y)

    # Create models
    encoder = Model(input_tensor, encoded, name="encoder")
    decoder = Model(input_encoded, decoded, name="decoder")
    autoencoder = Model(input_tensor, decoder(encoder(input_tensor)), name="autoencoder")

    return encoder, decoder, autoencoder


def create_deep_conv_ae(input_shape):

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
    _, _, ae = create_dense_ae((20, 4), 32)
    ae.summary()

    _, _, d_ae = create_deep_ae((1, 20, 4), 32)
    d_ae.summary()

    _, _, c_ae = create_deep_conv_ae((1, 20, 4), 32)
    c_ae.summary()
