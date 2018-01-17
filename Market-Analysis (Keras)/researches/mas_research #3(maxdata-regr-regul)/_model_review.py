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

# from keras.models import Model
from keras.utils import plot_model
from keras.models import model_from_json


def load_model(filename: str):
    """Loads the model from a text file."""

    json_string = ''
    try:
        file = open(filename, 'r')
    except IOError as exc:
        print('Error! Model file not find', exc)
    else:
        json_string = file.read()
        file.close()
    if len(json_string) > 0:
        model = model_from_json(json_string)
        return model


symbol = 'RMSprop-hinge_EURUSD1440'
file_model = symbol + '.model'
file_weights = symbol + '.hdf5'
file_png = '_' + symbol + '_model.png'

model = load_model(file_model)
model.load_weights(file_weights)

plot_model(model, to_file=file_png, show_shapes=True, show_layer_names=False)

text = ''
for item in model.layers:
    text = text + str(item.name) + '\n'
    text = text + str(item.input_shape) + '\n'
    text = text + str(item.output_shape) + '\n'
    text = text + str(item.get_weights()) + '\n'
    text = text + '\n=====================================\n'

# print(text)
nfile = open('_' + symbol + '_architecture.txt', 'w')
nfile.write(text)
nfile.close()

input('\nPress enter to exit...')


# import matplotlib.pyplot as plt
# input_w = model.get_layer(index=2).get_weights()[0][0]
# plt.plot(input_w)
# plt.show()
