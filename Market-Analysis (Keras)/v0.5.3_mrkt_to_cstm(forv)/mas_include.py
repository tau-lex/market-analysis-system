# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
#   Market Analysis System                                                    #
#   https://www.mql5.com/ru/users/terentyev23                                 #
#                                                                             #
#   M A R K E T   A N A L Y S I S   S C R I P T   W I T H   K E R A S         #
#                                                                             #
#   Aleksey Terentyev                                                         #
#   terentew.aleksey@ya.ru                                                    #
#                                                                             #
###############################################################################

import sys
import numpy as np
from keras.models import Model, Sequential, model_from_json


def get_parameters():
    """Returns a list of parameters."""
    idx = 0
    result = []
    for item in sys.argv:
        if idx > 0:
            result.append(item)
        idx += 1
    return result


def save_model(model: Model, filename: str):
    """Writes the model to a text file."""
    json_string = model.to_json()
    with open(filename+'.model', 'w') as file:
        file.write(json_string)


def load_model(filename: str):
    """Loads the model from a text file."""
    model = Sequential()
    json_string = ''
    try:
        file = open(filename+'.model', 'r')
    except IOError as exc:
        print('Error! Model file not find', exc)
    else:
        json_string = file.read()
        file.close()

    if( len(json_string) > 0 ):
        model = model_from_json( json_string )
    return model


def signal_to_class(signal_array):
    """Converts a list of signals to a two-dimensional list of classes."""
    result = np.array([], ndmin=2)
    for item in signal_array:
        if item > 0:
            result = np.append(result, [abs(item), 0.0])
        if item < 0:
            result = np.append(result, [0.0, abs(item)])
        if item == 0:
            result = np.append(result, [0.0, 0.0])
    return np.reshape(result, (signal_array.shape[0], 2))


def class_to_signal(class_array):
    """Converts a two-dimensional list of classes to a list of signals."""
    result = np.array([])
    for item in class_array:
        result = np.append(result, item[0] - item[1])
    return result
