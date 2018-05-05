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


def get_home():
    """Return directory path of user."""

    from os.path import expanduser

    return expanduser("~")


def get_parameters():
    """Returns a list of parameters (without filename)."""

    import sys

    return sys.argv[1:]


def get_script_dir(follow_symlinks=True):
    """
    Return script file directory.
    from: https://stackoverflow.com/questions/3718657/how-to-properly-determine-current-script-directory/22881871#22881871
    """

    import inspect
    import os
    import sys

    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)

    return os.path.dirname(path)


def plot_history(history):
    """Plot functions graph."""

    import matplotlib.pyplot as plt

    # summarize history for accuracy
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.axhline(y=0.5, color='grey', linestyle='--')
    plt.title('Model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.axhline(y=0.5, color='grey', linestyle='--')
    plt.title('Model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

