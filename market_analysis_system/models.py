# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
#   Market Analysis System                                                    #
#   https://www.mql5.com/ru/users/terentyev23                                 #
#                                                                             #
#   M A S   M O D E L S   F U N C T I O N                                     #
#                                                                             #
#   Aleksey Terentyev                                                         #
#   terentew.aleksey@ya.ru                                                    #
#                                                                             #
###############################################################################
"""
The module contains functions for working with the Keras models of the MAS project.
"""

from keras.models import Model, model_from_json #, Sequential


def save_model(model: Model, filename: str):
    """Writes the model to a text file."""

    json_string = model.to_json()

    with open(filename, 'w') as file:
        file.write(json_string)


def load_model(filename: str):
    """Loads the model from a text file."""

    # GOTO: load models from models lib
    # 'model/' + filename
    json_string = ''
    try:
        file = open(filename, 'r')
    except IOError as e:
        print('Error! Model file not found', e)
    else:
        json_string = file.read()
        file.close()
    if len(json_string) > 0:
        model = model_from_json(json_string)
        return model
