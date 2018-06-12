# -*- coding: utf-8 -*-
"""
The module contains functions for working with the Keras models of the MAS project.
"""

from keras.models import Model, Sequential
from keras.models import model_from_json
from keras.layers import Dense, Activation
from keras.layers import Flatten, BatchNormalization, Reshape
from keras.layers import LSTM


def save_model(model: Model, filename: str):
    """Writes the model to a text file."""

    json_string = model.to_json()

    with open(filename, 'w') as file:
        file.write(json_string)


def load_model(filename: str):
    """Loads the model from a text file."""

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
    """Simple model for RL."""

    model = Sequential()
    model.add(Reshape((input_shape[0], input_shape[1]), batch_input_shape=(None, 1, input_shape[0], input_shape[1])))
    model.add(BatchNormalization())
    # model.add(BatchNormalization(batch_input_shape=(None, input_shape[0], input_shape[1])))
    model.add(LSTM(16))
    model.add(Activation('relu'))
    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dense(nb_output, activation=act))

    return model


def simple_model2(input_shape, nb_output, act='linear'):
    """Simple model for RL."""

    model = Sequential()
    model.add(BatchNormalization(batch_input_shape=(None, input_shape)))
    model.add(LSTM(16))
    model.add(Activation('relu'))
    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dense(nb_output, activation=act))

    return model