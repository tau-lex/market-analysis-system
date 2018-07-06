# -*- coding: utf-8 -*-
"""
The module contains functions for working with the Keras models of the MAS project.
"""
from mas_tools.utils.ml import save_model_arch

from keras.models import model_from_json

from keras.models import Model, Sequential

from keras.layers import Input, concatenate, add
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


def cnn_model_2in(shape_a, shape_b, nb_output, activation='linear'):
    """CNN for exchange bot.
    
    # Arguments
        shape_a (): shape = (limit(timeseries or depth), features)
        shape_b (): shape = (limit(timeseries or depth), features)
        nb_output (int):
        activation (string): activation function for model output.
        
    Returns:
        model (keras.Model): Model of neural network."""

    assert shape_a[0] == shape_b[0]
    
    # Input A
    input_a = Input(shape=(1, shape_a[0], shape_a[1]),
                       name='input_a')
    # a = Reshape((shape_a[0], shape_a[1]))(input_a)
    a = BatchNormalization()(input_a)
    a = Conv2D(filters=96,
            kernel_size=(3, 1),
            padding='same',  # 'same' or 'causal'
            activation='relu',
            kernel_initializer='glorot_uniform',
            data_format='channels_first',
            )(a)
    # a = Flatten()(a)
    a = Reshape((shape_a[0], 96*shape_a[1]))(a)
    a = LSTM(64,
            activation='relu',
            kernel_initializer='glorot_uniform',
            return_sequences=True
            )(a)

    # Input B
    input_b = Input(shape=(1, shape_b[0], shape_b[1]),
                        name='input_b')
    # b = Reshape((shape_b[0], shape_b[1]))(input_b)
    b = BatchNormalization()(input_b)
    b = Conv2D(filters=96,
            kernel_size=(3, 1),
            padding='same',  # 'same' or 'causal'
            activation='relu',
            kernel_initializer='glorot_uniform',
            data_format='channels_first',
            )(b)
    # b = Flatten()(b)
    b = Reshape((shape_b[0], 96*shape_b[1]))(b)
    b = LSTM(64,
            activation='relu',
            kernel_initializer='glorot_uniform',
            return_sequences=True
            )(b)

    # x = add([a, b])
    x = concatenate([a, b])

    x = LSTM(96,
            activation='relu',
            kernel_initializer='glorot_uniform',
            return_sequences=True
            )(x)
    x = LSTM(32,
            activation='relu',
            kernel_initializer='glorot_uniform'
            )(x)
    # x = Dense(64, activation='relu')(x)
    output = Dense(nb_output, activation=activation)(x)

    model = Model(inputs=[input_a, input_b], outputs=output)

    return model


if __name__ == "__main__":
    path = 'E:/Projects/market-analysis-system/'

    model = simple_model((100, 4, 10), 3)
    save_model_arch(model, path+'simple')

    model = cnn_model_2in((50, 9), (50, 4), 3)
    save_model_arch(model, path+'cnn2in')

