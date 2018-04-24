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


def signal_to_class(data, n=2, normalize=True):
    """Converts a list of signals to a n-dimensional list of classes [buy, .., sell].
    normalize = True, it normalizes to unity.
    normalize = False, the signal changes only the sign."""

    result = np.array([], ndmin=n)
    data = np.array(data)

    if len(data.shape) > 1:
        print('signal_to_class() error')
        return None

    if n == 2:
        if normalize:
            for item in data:
                if item > 0:        # buy
                    result = np.append(result, [1.0, 0.0])
                if item < 0:        # sell
                    result = np.append(result, [0.0, 1.0])
                if item == 0:       # pass
                    result = np.append(result, [0.0, 0.0])
        else:
            for item in data:
                result = np.append(result, [0.5+item/2.0, 0.5-item/2.0])
    elif n == 3:
        if normalize:
            for item in data:
                if item > 0:        # buy
                    result = np.append(result, [1.0, 0.0, 0.0])
                if item < 0:        # sell
                    result = np.append(result, [0.0, 0.0, 1.0])
                if item == 0:       # pass
                    result = np.append(result, [0.0, 1.0, 0.0])
        else:
            for item in data:
                if item > 0:        # buy
                    result = np.append(result, [abs(item), (1.0-abs(item)), 0.0])
                if item < 0:        # sell
                    result = np.append(result, [0.0, (1.0-abs(item)), abs(item)])
                if item == 0:       # pass
                    result = np.append(result, [0.0, 1.0, 0.0])

    return np.reshape(result, (data.shape[0], n))


def class_to_signal(data, n=2, normalized=True):
    """Converts a n-dimensional list of classes to a list of signals."""

    result = np.array([])

    if n == 2:
        if normalized:
            for item in data:
                result = np.append(result, item[0] - item[1])
        else:
            for item in data:
                result = np.append(result, item[0] * 2 - 1.0)
    elif n == 3:
        if normalized:
            for item in data:
                if item[0] > item[1] and item[0] > item[2]:
                    result = np.append(result, 1.0)
                elif item[2] > item[1] and item[2] > item[0]:
                    result = np.append(result, -1.0)
                elif item[1] > item[0] and item[1] > item[2]:
                    result = np.append(result, 0.0)
        else:
            for item in data:
                if item[0] > item[1] and item[0] > item[2]:
                    result = np.append(result, item[0])
                elif item[2] > item[1] and item[2] > item[0]:
                    result = np.append(result, -item[2])
                elif item[1] > item[0] and item[1] > item[2]:
                    result = np.append(result, 0.0)

    return result

