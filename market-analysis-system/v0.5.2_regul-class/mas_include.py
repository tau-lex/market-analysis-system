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
from keras.models import Model, model_from_json#, Sequential


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
    """ Writes the model to a text file. """
    json_string = model.to_json()
    with open(filename+'.model', 'w') as file:
        file.write(json_string)


def load_model(filename: str):
    """ Loads the model from a text file. """
    json_string = ''
    try:
        file = open(filename+'.model', 'r')
    except IOError as exc:
        print('Error! Model file not find', exc)
    else:
        json_string = file.read()
        file.close()
    if len(json_string) > 0:
        model = model_from_json(json_string)
        return model


def create_timeseries_matrix(data_x, data_y = [], look_back = 3):
    """ Convert an array of values into a dataset matrix """
    if look_back <= 1:
        return np.array(data_x), np.array(data_y)
    if look_back >= data_x.shape[0]:
        print('create_timeseries_matrix() error')
        return None
    result = np.array([])
    for i in range(len(data_x) - look_back + 1):
        row = data_x[i:(i + look_back), :]
        np.reshape(row, data_x.shape[1] * look_back)
        result = np.append(result, row)
    new_shape = (data_x.shape[0] - look_back + 1, data_x.shape[1] * look_back)
    result = np.reshape(result, new_shape)
    return np.array(result), np.array(data_y[look_back - 1:])


def get_delta(data, index1=0, index2=1):
    result = []
    for item in data:
        result.append(item[index1] - item[index2])
    return np.array(result)


def get_delta_from_ohlc(data, index1=0, index2=3):
    result = []
    for row in data:
        # delta open - close, high - low, high - open, close - low
        pass
    return np.array(result)


def signal_to_class2(signal_array):
    """ Converts a list of signals to a two-dimensional list of classes [buy, sell]."""
    result = np.array([], ndmin=2)
    for item in signal_array:
        result = np.append(result, [0.5+item/2.0, 0.5-item/2.0])
    return np.reshape(result, (signal_array.shape[0], 2))


def class2_to_signal(class_array):
    """Converts a two-dimensional list of classes to a list of signals."""
    result = np.array([])
    for item in class_array:
        result = np.append(result, item[0] - item[1])
    return result


def signal_to_class3(signal_array):
    """Converts a list of signals to a three-dimensional list of classes [buy, pass, sell]."""
    result = np.array([], ndmin=2)
    for item in signal_array:
        if item > 0:        # buy
            result = np.append(result, [abs(item), (1.0-abs(item)), 0.0])
        if item < 0:        # sell
            result = np.append(result, [0.0, (1.0-abs(item)), abs(item)])
        if item == 0:       # pass
            result = np.append(result, [0.0, 1.0, 0.0])
    return np.reshape(result, (signal_array.shape[0], 3))


def class3_to_signal(class_array):
    """Converts a three-dimensional list of classes to a list of signals."""
    result = np.array([])
    for item in class_array:
        if item[0] > item[2]:
            result = np.append(result, abs(item[0]))
        elif item[0] < item[2]:
            result = np.append(result, 0.0-abs(item[2]))
        else:
            result = np.append(result, 0.0)
#        result = np.append(result, item[0] - item[2])
    return result

