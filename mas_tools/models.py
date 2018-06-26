# -*- coding: utf-8 -*-
"""
The module contains functions for working with the Keras models of the MAS project.
"""
from mas_tools.utils.ml import save_model_arch

from keras.models import model_from_json

from keras.models import Model, Sequential

from keras.layers import Input, concatenate
from keras.layers import Dense, Activation
from keras.layers import LSTM, GRU
from keras.layers import BatchNormalization, Dropout
from keras.layers import Flatten, Reshape

from keras.layers import Conv1D, Conv2D
from keras.layers import AveragePooling1D, MaxPooling1D
from keras.layers import GlobalAveragePooling1D, GlobalMaxPooling1D

from keras.activations import relu


def save_model(model: Model, filename: str):
    """Writes the model to a text file.
    
    # Arguments
        model (keras.Model): Model of the neural network to save.
        file (str): Path and filename."""

    json_string = model.to_json()

    with open(filename, 'w') as file:
        file.write(json_string)


def load_model(filename: str):
    """Loads the model from a text file.
    
    Arguments
        file (str): Path and filename.
        
    Returns:
        model (keras.Model): Model of neural network."""

    json_string = ''
    try:
        file = open(filename, 'r')
    except IOError as e:
        print('Model file not found', e)
    else:
        json_string = file.read()
        file.close()
    if len(json_string) > 0:
        model = model_from_json(json_string)
        return model


def simple_model(input_shape, nb_output, act='linear'):
    """Simple model for RL.
        
    Returns:
        model (keras.Model): Model of neural network."""

    model = Sequential()
    # model.add(Reshape((input_shape[1], input_shape[2]),
    #                     batch_input_shape=(None, 1, input_shape[0], input_shape[1], input_shape[2])))
    # model.add(BatchNormalization())
    model.add(BatchNormalization(batch_input_shape=(None, input_shape[0], input_shape[1])))
    model.add(LSTM(input_shape[1] * input_shape[2]))
    model.add(Activation('relu'))
    model.add(Dropout(0.4))
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.4))
    model.add(Dense(32))
    model.add(Activation('relu'))
    model.add(Dropout(0.4))
    model.add(Dense(nb_output, activation=act))

    return model


def two_inputs_cnn_model(candles_shape, tickers_shape, nb_output, activation='linear'):
    """CNN for exchange bot.
    
    # Arguments
        candles_shape (): 
        tickers_shape (): 
        nb_output (int):
        activation (string): activation function for model output.
        
    Returns:
        model (keras.Model): Model of neural network."""
    
    # candles shape = (9, limit(50, 100, ))
    candles_in = Input(shape=(candles_shape[0], candles_shape[1]),
                       name='candles_input')
    a = BatchNormalization()(candles_in)
    a = Conv1D(filters=16,
               kernel_size=2,
               padding='same',                  # 'same' or 'causal'
            #    data_format='channels_first',    # channels is o,h,l,c,etc; length is limit
              )(a)
    a = LSTM(16, activation='relu')(a)
    # a = relu(a, max_value=1.0)(a)

    # tickers shape = (4, limit(50, 100, ))
    tickers_in = Input(shape=(tickers_shape[0], tickers_shape[1]),
                       name='tickers_input')
    b = BatchNormalization()(tickers_in)
    b = Conv1D(filters=16,
               kernel_size=2,
               padding='same',                  # 'same' or 'causal'
            #    data_format='channels_first',    # channels is o,h,l,c,etc; length is limit
              )(b)
    b = LSTM(16, activation='relu')(b)
    # b = relu(b, max_value=1.0)(b)

    x = concatenate([a, b])
    # x = Merge([a, b], , mode='concat')

    x = Dense(32, activation='relu')(x)
    # x = relu(x, max_value=1.0)(x)
    x = Dense(16, activation='relu')(x)
    # x = relu(x, max_value=1.0)(x)
    output = Dense(nb_output, activation=activation)(x)

    model = Model(inputs=[candles_in, tickers_in], outputs=output)

    return model


if __name__ == "__main__":
    path = 'E:/Projects/market-analysis-system/'

    model = simple_model((100, 4, 10), 3)
    save_model_arch(model, path+'simple')

    model = two_inputs_cnn_model((9, 50), (4, 50), 3)
    save_model_arch(model, path+'cnn2in')

