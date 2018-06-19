# -*- coding: utf-8 -*-
"""
The module contains the data processing functions.
"""

import numpy as np


def signal_to_class(data, n=2, normalize=True):
    """
    Converts a list of signals to a n-dimensional list of classes [buy, .., sell].

    Arguments:
        n (int): Number of classes.
        normalize (bool): It normalizes to unity. False - the signal changes only the sign.
        
    Returns:
        Array of classes.
    """

    result = np.array([])
    data = np.array(data)

    if len(data.shape) > 1:
        raise ValueError("The array must be one-dimensional.")

    if n == 2:
        if normalize:
            for item in data:
                if item > 0:        # buy
                    result = np.append(result, [1.0, 0.0])
                if item < 0:        # sell
                    result = np.append(result, [0.0, 1.0])
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
    elif n == 6:
        for item in data:
            if item >= 0.8 and item <= 1.0:
                result = np.append(result, [1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            elif item >= 0.4 and item < 0.8:
                result = np.append(result, [0.0, 1.0, 0.0, 0.0, 0.0, 0.0])
            elif item >= 0.0 and item < 0.4:
                result = np.append(result, [0.0, 0.0, 1.0, 0.0, 0.0, 0.0])
            elif item > -0.4 and item < 0.0:
                result = np.append(result, [0.0, 0.0, 0.0, 1.0, 0.0, 0.0])
            elif item > -0.8 and item <= 0.4:
                result = np.append(result, [0.0, 0.0, 0.0, 0.0, 1.0, 0.0])
            elif item >= -1.0 and item <= 0.8:
                result = np.append(result, [0.0, 0.0, 0.0, 0.0, 0.0, 1.0])

    return result.reshape((data.shape[0], n))


def class_to_signal(data, n=2, normalized=True):
    """Converts a n-dimensional list of classes to a list of signals."""

    result = np.array([])

    if n == 2:
        if normalized:
            for item in data:
                result = np.append(result, 1 if item[0] > item[1] else -1)
        else:
            for item in data:
                result = np.append(result, item[0] * 2 - 1.0)
    elif n == 3:
        if normalized:
            for item in data:
                _class = np.argmax(item)
                if _class == 0:
                    result = np.append(result, 1.0)
                elif _class == 1:
                    result = np.append(result, 0.0)
                elif _class == 2:
                    result = np.append(result, -1.0)
        else:
            for item in data:
                _class = np.argmax(item)
                if _class == 0:
                    result = np.append(result, item[0])
                elif _class == 1:
                    result = np.append(result, 0.0)
                elif _class == 2:
                    result = np.append(result, -item[2])
    elif n == 6:
        for item in data:
            _class = np.argmax(item)
            if _class == 0:
                result = np.append(result, 1.0)
            elif _class == 1:
                result = np.append(result, 0.66)
            elif _class == 2:
                result = np.append(result, 0.33)
            elif _class == 3:
                result = np.append(result, -0.33)
            elif _class == 4:
                result = np.append(result, -0.66)
            elif _class == 5:
                result = np.append(result, -1.0)

    return result


def prepare_target(data, close_index=3, classes=6):
    """
    Hello (=
    uniform classes
    """
    # TODO
    # while const
    classes = 6
    
    data = np.array(data)
    new_target = data[1:, close_index] / data[:-1, close_index]
    new_target = np.insert(new_target, obj=0, values=[1.0])
    
    n, bins = np.histogram(new_target, bins=200, range=(0.99, 1.01))
    
    sixth = sum(n) / classes
    
    points = [0., 0., 1., 0., 0.]
    _sum = n[100]/2
    p_idx = 1
    for idx in range(99, -1):
        _sum += n[idx]
        if _sum >= sixth:
            points[p_idx] = (idx - 100) / 10**4 + 1
            p_idx -= 1
        if p_idx < 0:
            break
    _sum = n[100]/2
    p_idx = 3
    for idx in range(101, 201):
        _sum += n[idx]
        if _sum >= sixth:
            points[p_idx] = (idx - 100) / 10**4 + 1
            p_idx += 1
        if p_idx > 4:
            break
    # TODO
    def select(a):
        a > points[2]
        return 1
    new_target = [select(x) for x in new_target]

    return new_target


def print_classification_scores(true_y, test_y, n=3):
    """"""

    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import classification_report
    from sklearn.metrics import matthews_corrcoef

    print('-' * 20)
    if n == 2:
        print('\nMATTHEWS CORRELATION')
        print(matthews_corrcoef(true_y, test_y))
        CM = confusion_matrix(true_y, test_y, labels=[0, 1])
        print('\nCONFUSION MATRIX')
        print(CM / CM.astype(np.float).sum(axis=1))
        print('\nCLASSIFICATION REPORT')
        print(classification_report(true_y, test_y,
                                    labels=[0, 1],
                                    target_names=['zero', 'one']))
    elif n == 3:
        print('\nMATTHEWS CORRELATION')
        print(matthews_corrcoef(true_y, test_y))
        CM = confusion_matrix(true_y, test_y, labels=[0, 1, 2])
        print('\nCONFUSION MATRIX')
        print(CM / CM.astype(np.float).sum(axis=1))
        print('\nCLASSIFICATION REPORT')
        print(classification_report(true_y, test_y,
                                    labels=[0, 1, 2],
                                    target_names=['buy', 'hold', 'sell']))
    elif n == 6:
        print('\nMATTHEWS CORRELATION')
        print(matthews_corrcoef(true_y, test_y))
        CM = confusion_matrix(true_y, test_y, labels=[0, 1, 2, 3, 4, 5])
        print('\nCONFUSION MATRIX')
        print(CM / CM.astype(np.float).sum(axis=1))
        print('\nCLASSIFICATION REPORT')
        print(classification_report(true_y, test_y,
                                    labels=[0, 1, 2, 3, 4, 5],
                                    target_names=['buy', 'med', 'hold', '-hold', '-med', 'sell']))
    print('-' * 20)

