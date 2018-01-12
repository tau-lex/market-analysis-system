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

from mas.models import load_model
# from keras.models import Model
from keras.utils import plot_model


symbol = 'simple_rnn_EURUSD.pro1440'
file_model = symbol + '.model'
file_weights = symbol + '.hdf5'
file_png = symbol + '_model.png'

model = load_model(file_model)
model.load_weights(file_weights)

plot_model(model, to_file=file_png, show_shapes=True, show_layer_names=False)

for item in model.layers:
    print(item.name)
    print(item.input_shape)
    print(item.output_shape)
    print('\n')
    print(item.weights)
    print('\n===\n')

# model.get_layer(index=2).get_weights().shape
