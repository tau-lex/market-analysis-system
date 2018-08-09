# -*- coding: utf-8 -*-
from mas_tools.ml import save_model_arch

from keras.models import model_from_json

from keras.models import Model, Sequential

from keras.layers import Input, concatenate, add
from keras.layers import Dense, Activation
from keras.layers import LSTM, GRU
from keras.layers import BatchNormalization, Dropout
from keras.layers import Flatten, Reshape

from mas_tools.layers import Attention, AttentionWithContext, AttentionWeightedAverage

from keras.activations import relu


def save_model(model: Model, filename: str):
    """Writes the model to a text file.
    
    Arguments
        model (keras.Model): Model of the neural network to save.
        file (str): Path and filename."""

    json_string = model.to_json()

    with open(filename, 'w') as file:
        file.write(json_string)


def load_model(filename: str):
    """Loads the model from a text file.
    
    Arguments
        file (str): Path and filename.
        
    Returns
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
        
    Returns
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


if __name__ == "__main__":
    path = 'E:/Projects/market-analysis-system/'

    model = simple_model((100, 4, 10), 3)
    save_model_arch(model, path+'simple')
    model.summary()
