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


def signal_to_class2(data, normalize=True):
    """Converts a list of signals to a two-dimensional list of classes [buy, sell].
    normalize = True, it normalizes to unity.
    normalize = False, the signal changes only the sign."""

    result = np.array([], ndmin=2)
    data = np.array(data)

    if len(data.shape) > 1:
        print('signal_to_class2() error')
        return None

    if normalize:
        for item in data:
            result = np.append(result, [0.5+item/2.0, 0.5-item/2.0])
    else:
        for item in data:
            if item > 0:
                result = np.append(result, [abs(item), 0.0])
            if item < 0:
                result = np.append(result, [0.0, abs(item)])
            if item == 0:
                result = np.append(result, [0.0, 0.0])

    return np.reshape(result, (data.shape[0], 2))


def class2_to_signal(data, normalized=True):
    """Converts a two-dimensional list of classes to a list of signals."""

    result = np.array([])

    if normalized:
        for item in data:
            result = np.append(result, item[0] * 2 - 1.0)
    else:
        for item in data:
            result = np.append(result, item[0] - item[1])

    return result


def signal_to_class3(data):
    """Converts a list of signals to a three-dimensional list of classes [buy, pass, sell]."""

    result = np.array([], ndmin=2)

    for item in data:
        if item > 0:        # buy
            result = np.append(result, [abs(item), (1.0-abs(item)), 0.0])
        if item < 0:        # sell
            result = np.append(result, [0.0, (1.0-abs(item)), abs(item)])
        if item == 0:       # pass
            result = np.append(result, [0.0, 1.0, 0.0])

    return np.reshape(result, (data.shape[0], 3))


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

    return result


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
    
    return np.diff(data, rate)
