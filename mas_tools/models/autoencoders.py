from keras.models import Model
from keras.layers import Input, Dense, concatenate, Lambda
from keras.layers import Flatten, Reshape, BatchNormalization, Dropout
from keras.layers import Conv2D, MaxPooling2D, Conv2DTranspose, UpSampling2D
from keras.losses import mse, mae, mape, binary_crossentropy
from keras.regularizers import L1L2
from keras import backend as K


def dense_ae(input_shape, encoding_dim=64, output_activation='linear'):
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


def deep_ae(input_shape, encoding_dim=64,
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


def deep_conv_ae(input_shape, latent_dim=32):
    """"""
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
                    latent_dim=100,
                    filters_count=(8, 24),
                    dropout = 0.3):
    """"""
    kernel_size = (3, 3)
    kernel_pooling = (2, 2)
    strides = (1, 1)
    initializer = 'truncated_normal'
    
    # Encoder
    input_tensor = Input(shape=input_shape, name='encoder_input')
    if len(input_shape) == 2:
        x = Reshape((input_shape[0], input_shape[1], 1))(input_tensor)
    elif len(input_shape) == 3:
        x = input_tensor
    x = Conv2D(filters=filters_count[0],
                kernel_size=kernel_size,
                padding='same',
                activation='relu',
                kernel_initializer=initializer,
                strides=strides)(x)
    x = Dropout(dropout)(x)
    x = MaxPooling2D(kernel_pooling)(x)
    x = Conv2D(filters=filters_count[1],
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
    x = Dense(latent_dim*3, activation='relu', name='encoder_output')(x)

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
    y = Conv2DTranspose(filters=filters_count[1],
                    kernel_size=kernel_size,
                    padding='same',
                    activation='relu',
                    kernel_initializer=initializer,
                    strides=strides)(y)
    y = UpSampling2D(kernel_pooling)(y)
    y = Dropout(dropout)(y)
    y = Conv2DTranspose(filters=filters_count[0],
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
    _, _, ae = dense_ae((20, 4), 32)
    ae.summary()

    _, _, d_ae = deep_ae((1, 20, 4), 32)
    d_ae.summary()

    _, _, c_ae = deep_conv_ae((1, 20, 4), 32)
    c_ae.summary()

    _, _, vae, _ = deep_conv2d_vae((100, 100, 3) )
    vae.summary()
