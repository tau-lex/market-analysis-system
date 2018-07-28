from keras.models import Model
from keras.layers import Input, Dense, Flatten, Reshape
from keras.layers import Conv2D, MaxPooling2D, UpSampling2D
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


def create_deep_conv_ae():
    # TODO
    input_img = Input(shape=(28, 28, 1))

    x = Conv2D(128, (7, 7), activation='relu', padding='same')(input_img)
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Conv2D(32, (2, 2), activation='relu', padding='same')(x)
    x = MaxPooling2D((2, 2), padding='same')(x)
    encoded = Conv2D(1, (7, 7), activation='relu', padding='same')(x)

    # На этом моменте представление  (7, 7, 1) т.е. 49-размерное

    input_encoded = Input(shape=(7, 7, 1))
    x = Conv2D(32, (7, 7), activation='relu', padding='same')(input_encoded)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(128, (2, 2), activation='relu', padding='same')(x)
    x = UpSampling2D((2, 2))(x)
    decoded = Conv2D(1, (7, 7), activation='sigmoid', padding='same')(x)

    # Create models
    encoder = Model(input_img, encoded, name="encoder")
    decoder = Model(input_encoded, decoded, name="decoder")
    autoencoder = Model(input_img, decoder(encoder(input_img)), name="autoencoder")

    return encoder, decoder, autoencoder


if __name__ == "__main__":
    _, _, ae = create_dense_ae((20, 4), 32)
    ae.summary()

    _, _, d_ae = create_deep_ae((1, 20, 4), 32)
    d_ae.summary()

    _, _, c_ae = create_deep_conv_ae((1, 20, 4), 32)
    c_ae.summary()
