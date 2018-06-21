# -*- coding: utf-8 -*-
"""
The module contains functions for the MAS project.
"""

import inspect
import os
import sys

import numpy as np

import matplotlib.pyplot as plt


def get_home():
    """Return directory path of user."""

    return os.path.expanduser("~")


def get_parameters():
    """Returns a list of parameters (without filename)."""

    return sys.argv[1:]


def get_script_dir(follow_symlinks=True):
    """
    Return script file directory.
    from: https://stackoverflow.com/questions/3718657/how-to-properly-determine-current-script-directory/22881871#22881871
    """

    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)

    return os.path.dirname(path)


def plot_history(history, acc='accuracy'):
    """Plot functions graph."""

    import matplotlib.pyplot as plt

    # summarize history for accuracy
    plt.plot(history.history[acc])
    plt.plot(history.history['val_'+acc])
    # plt.axhline(y=0.5, color='grey', linestyle='--')
    plt.title('Model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    # plt.axhline(y=0.5, color='grey', linestyle='--')
    plt.title('Model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    plt.figure()
    
    print(cm)
    
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(classes)
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def calculate_stop_loss(data, direction: str, position=0, factor=3.0):
    """Calculates the price of a stop order on an array of the latest prices.

    The minimum size of the history of the 12 last candles,
    including the bar for which the stop level is calculated,
    i.e. the size of the array must be more than 12.
    The method is described by Alexander Elder.

    # Arguments
        data (list): an array of prices, the size of (n, 1) or (n, 4),
                where n is greater than or equal to 12.
        position (int): row index for calculate stop level.
        direction (str): direction, 'buy/sell', 'up/down'.
    # Returns
        stop_price (float): The price of the breakdown in the opposite direction,
        at which it is necessary to close the position.
    """

    buy = ['buy', 'up']
    sell = ['sell', 'sale', 'down']
    if direction.lower() not in buy and direction.lower() not in sell:
        raise ValueError('Illegal argument direction.')
    if len(data) < 12:
        # raise ValueError('To short')
        return 0.0

    data = np.array(data[position-12:position-1])

    if len(data.shape) == 2:
        if data.shape[1] == 1:
            data = data[:, 0]
        elif data.shape[1] == 4:
            if direction.lower() in buy:
                data = data[:, 2] # low
            elif direction.lower() in sell:
                data = data[:, 1] # high
        else:
            raise ValueError('Array shape is not correct.')

    sum_bd = 0.0
    count_bd = 0
    bd_data = np.diff(data)
    if direction.lower() in buy:
        for item in bd_data:
            if item < 0:
                sum_bd += abs(item)
                count_bd += 1
        stop_price = data[position-2] - abs(bd_data[-1]) * factor
        if count_bd > 0:
            stop_price = data[position-2] - (sum_bd / count_bd) * factor
    elif direction.lower() in sell:
        for item in bd_data:
            if item > 0:
                sum_bd += item
                count_bd += 1
        stop_price = data[position-2] + abs(bd_data[-1]) * factor
        if count_bd > 0:
            stop_price = data[position-2] + (sum_bd / count_bd) * factor

    return stop_price


def calculate_lot(one_lot_risk, balance_risk, min_lot, precision=2):
    """Calculates the size of lot by the size of risk.
    Be careful, the risk values must be calculated in one currency.
    
    Arguments:
        one_lot_risk: Risk when buying a single lot. It can be calculated
                        as the absolute difference between the purchase price and the stop loss.
        balance_risk: Fixed risk for the current balance.
        min_lot: Minimum order size.
    """
    
    if one_lot_risk * min_lot >= balance_risk or one_lot_risk <= 0:
        return min_lot
    elif min_lot == 1:
        return floor(balance_risk / one_lot_risk)
    else:
        return round(balance_risk / one_lot_risk - min_lot, precision)
    return -1.0


def adjust_to_step(self, value, step, increase=False):
    """Rounds any number to a multiple of the specified step.

    from: https://bablofil.ru

    Arguments:
        increase (bool): if True - rounding will occur to a larger step value.
    """

    return ((int(value * 100000000) - int(value * 100000000) % int(
            float(step) * 100000000)) / 100000000)+(float(step) if increase else 0)
