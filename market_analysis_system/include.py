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
"""
The module contains functions for the MAS project.
"""

import sys
import matplotlib.pyplot as plt


def get_parameters():
    """Returns a list of parameters."""

    idx = 0
    result = []

    for item in sys.argv:
        if idx > 0:
            result.append(item)
        idx += 1

    return result


def plot_history(history):
    """Plot functions graph"""

    # summarize history for accuracy
    # plt.subplot(2, 1, 1)
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.axhline(y=0.5, color='grey', linestyle='--')
    plt.title('Model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    # summarize history for loss
    # plt.subplot(2, 1, 2)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.axhline(y=0.693, color='grey', linestyle='--')
    plt.title('Model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

