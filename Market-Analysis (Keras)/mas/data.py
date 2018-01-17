# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
#   Market Analysis System                                                    #
#   https://www.mql5.com/ru/users/terentyev23                                 #
#                                                                             #
#   M A S   D A T A   F U N C T I O N                                         #
#                                                                             #
#   Aleksey Terentyev                                                         #
#   terentew.aleksey@ya.ru                                                    #
#                                                                             #
###############################################################################
"""
The module contains the data processing functions of the MAS project.
"""

from math import exp
import numpy as np


def create_timeseries_matrix(data_x, data_y=np.array([]), look_back=3):
    """Converts a dataset into a time series matrix."""

    if look_back <= 1:
        return np.array(data_x), np.array(data_y)

    if look_back >= data_x.shape[0]:
        print('create_timeseries_matrix() error')
        return None

    result = np.array([])
    data_x = np.array(data_x)
    data_y = np.array(data_y)

    for i in range(len(data_x) - look_back + 1):
        row = data_x[i:(i + look_back), :]
        np.reshape(row, data_x.shape[1] * look_back)
        result = np.append(result, row)

    new_shape = (data_x.shape[0] - look_back + 1, data_x.shape[1] * look_back)
    result = np.reshape(result, new_shape)

    return result, data_y[look_back - 1:]


def dataset_to_traintest(data, ratio=0.6, limit=0):
    """Returns a data set divided into two matrices.
    train = ratio * data.
    limit > 0 - limits the size of the dataset."""

    data = np.array(data)

    start, size = 0, len(data)
    if limit > 0:
        if size > limit:
            start, size = size - limit, limit

    if ratio <= 0.0:
        return None, data[start:len(data), :]
    elif ratio >= 1.0:
        return data[start:len(data), :], None

    train_size = int(size * ratio)
    # test_size = len(data) - train_size

    if len(data.shape) == 1:
        return data[start:(start + train_size),], data[(start + train_size):len(data),]
    return data[start:(start + train_size), :], data[(start + train_size):len(data), :]


def get_delta(data, index1=0, index2=1):
    """Returns the difference between index1 and index2."""

    result = np.array([])

    for item in data:
        result = np.append(result, item[index1] - item[index2])

    return result


def get_deltas_from_ohlc(data, index1=0):
    """Calculates the delta prices (open, high, low, close) between index1 and index2.
    Returns the numpy array with the shape (x, 6): [O-C, H-L, H-O, H-C, O-L, C-L]"""

    result = np.array([])
    data = np.array(data)

    for item in data:
        result = np.append(result, [item[index1] - item[index1 + 3],    # Open - Close
                                    item[index1 + 1] - item[index1 + 2],# High - Low
                                    item[index1 + 1] - item[index1],    # High - Open
                                    item[index1 + 1] - item[index1 + 3],# High - Close
                                    item[index1] - item[index1 + 2],    # Open - Low
                                    item[index1 + 3] - item[index1 + 2] # Close - Low
                                   ])

    return np.reshape(result, (data.shape[0], 6))


def get_diff(data, rate=1):
    """Calculates a derivative and returns an array of length equal to
	the length of the original array."""

    result = np.diff(data, rate)

    for idx in range(rate):
        result = np.append(result, 0.0)

    return result


def get_sigmoid(data):
    """Sigmoid function."""

    result = 1 / (1 + np.exp(-data))

    return result


def get_sigmoid_to_zero(data):
    """Sigmoid function."""

    result = 1 / (1 + np.exp(-data)) - 0.5

    return result


def get_sigmoid0(data):
    """Numerically-stable sigmoid function."""

    result = np.array([])
    z = 0.0

    for item in data:
        if item >= 0.0:
            z = 1.0 / (1 + exp(-data))
        else:
            z = 1.0 / (1 + exp(data))
        result = np.append(result, z)

    return result


def get_sigmoid1(data):
    """More variant."""

    return exp(-np.logaddexp(0, -data))


def get_sigmoid2(data):
    """More variant."""

    return 0.5 * (1 + data / (1 + abs(data)))
