# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
#   Market Analysis System                                                    #
#   https://www.mql5.com/ru/users/terentyev23                                 #
#                                                                             #
#   M A S   D A T A   F U N C T I O N S                                       #
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


def create_timeseries_matrix(data_x, data_y=[], look_back=3):
    """Converts a dataset into a time series matrix."""

    if look_back <= 1:
        return np.array(data_x), np.array(data_y)

    if look_back >= data_x.shape[0]:
        print('create_timeseries_matrix() error = look back size is large')
        return None

    result = np.array([])
    data_x = np.array(data_x)
    data_y = np.array(data_y)

    for idx in range(len(data_x) - look_back + 1):
        row = data_x[idx:(idx + look_back), :]
        np.reshape(row, data_x.shape[1] * look_back)
        result = np.append(result, row)

    new_shape = (data_x.shape[0] - look_back + 1, data_x.shape[1] * look_back)
    result = np.reshape(result, new_shape)

    return result, data_y[look_back-1:]


def dataset_to_traintest(data, train_ratio=0.6, limit=0):
    """Returns a data set divided into two matrices.
    train = train_ratio * data.
    limit > 0 - limits the size of the dataset."""

    data = np.array(data)

    start, size = 0, len(data)
    if limit > 0:
        if size > limit:
            start, size = size - limit, limit
    elif limit < 0:
        if size > abs(limit):
            start, size = 0, abs(limit)

    if train_ratio <= 0.0:
        return None, data[start:size, :]
    elif train_ratio >= 1.0:
        return data[start:size, :], None

    train_size = int(size * train_ratio)
    # test_size = len(data) - train_size

    if len(data.shape) == 1:
        return data[start:(start + train_size),], data[(start + train_size):len(data),]
    return data[start:(start + train_size), :], data[(start + train_size):len(data), :]


def shuffle_xy(data_a = [], data_b = []):
    """Shuffle data sets."""

    data_a = np.array(data_a)
    data_b = np.array(data_b)
    width_a = data_a.shape[1]
    # if len(data_b.shape) > 1:
    #     width_b = data_b.shape[1]
    # else:
    #     width_b = data_b.shape[0]
    # if width_a != width_b:
    #     print()
    #     return ([], [])
    temp = np.column_stack((data_a, data_b))
    np.random.shuffle(temp)

    return np.hsplit(temp, np.array([width_a]))


def get_delta(data, index1=0, index2=1):
    """Returns the difference between [,index1] and [,index2] in 2-D array."""

    return data[:, index1] - data[:, index2]


def get_deltas_from_ohlc(data, index1=0):
    """Calculates the delta prices (open, high, low, close) between index1 and index2.
    Returns the numpy array with the shape (:, 6): [O-C, H-L, H-O, H-C, O-L, C-L]"""

    return np.column_stack((get_delta(data, index1, index1 + 3),    # Open - Close
                                get_delta(data, index1 + 1, index1 + 2),# High - Low
                                get_delta(data, index1 + 1, index1),    # High - Open
                                get_delta(data, index1 + 1, index1 + 3),# High - Close
                                get_delta(data, index1, index1 + 2),    # Open - Low
                                get_delta(data, index1 + 3, index1 + 2) # Close - Low
                            ))


def get_diff(data, rate=1):
    """Computes a derivative and returns an array equal to
    the length of the original array."""

    result = np.array([])
    for idx in range(rate):
        result = np.append(result, 0.0)

    if rate == 1:
        return np.append(result, np.diff(data))

    for idx in range(rate, len(data)):
        result = np.append(result, data[idx] - data[idx-rate])

    return result


def get_log_diff(data, rate=1):
    """Computes the log-differential and returns an array equal to
    the length of the original array."""

    result = np.array([])
    for idx in range(rate):
        result = np.append(result, 0.0)

    for idx in range(rate, len(data)):
        ld = np.log(data[idx] / data[idx-rate])
        result = np.append(result, ld)

    return result


def get_sigmoid(data):
    """Sigmoid function."""

    result = 1 / (1 + np.exp(-data))
    # return exp(-np.logaddexp(0, -data))
    # return 0.5 * (1 + data / (1 + abs(data)))

    return result


def get_sigmoid_to_zero(data):
    """Sigmoid function."""

    result = 1 / (1 + np.exp(-data)) - 0.5

    return result


def get_sigmoid_stable(data):
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


def get_sigmoid_ration(data, alpha=2.0):
    """Rationaly sigmoid."""

    result = data / (np.abs(data) + alpha)

    return result
