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


def signal_to_class3(data, normalize=True):
    """Converts a list of signals to a three-dimensional list of classes [buy, pass, sell]."""

    result = np.array([], ndmin=3)

    if normalize:
        for item in data:
            if item > 0:        # buy
                result = np.append(result, [abs(item), (1.0-abs(item)), 0.0])
            if item < 0:        # sell
                result = np.append(result, [0.0, (1.0-abs(item)), abs(item)])
            if item == 0:       # pass
                result = np.append(result, [0.0, 1.0, 0.0])
    else:
        for item in data:
            if item > 0:        # buy
                result = np.append(result, [1.0, 0.0, 0.0])
            if item < 0:        # sell
                result = np.append(result, [0.0, 0.0, 1.0])
            if item == 0:       # pass
                result = np.append(result, [0.0, 1.0, 0.0])


    return np.reshape(result, (data.shape[0], 3))


def class3_to_signal(class_array, normalized=True):
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
