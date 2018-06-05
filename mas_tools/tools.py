# -*- coding: utf-8 -*-
"""
The module contains functions for the MAS project.
"""

import inspect
import os
import sys

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
