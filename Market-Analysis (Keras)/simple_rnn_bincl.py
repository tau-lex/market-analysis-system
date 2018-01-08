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

from __future__ import print_function
import math
import matplotlib.pyplot as plt
import numpy as np

from mas.include import get_parameters
from mas.data import signal_to_class2, class2_to_signal
from mas.data import create_timeseries_matrix, dataset_to_traintest
from mas.models import save_model, load_model

from keras.models import Sequential
from keras.layers import Dense, GRU, Dropout, Activation
from keras.layers import BatchNormalization
from keras.layers import LeakyReLU
from keras.optimizers import Nadam, RMSprop, Adam, SGD
from keras.callbacks import ReduceLROnPlateau
from keras import regularizers
from sklearn.metrics import mean_squared_error


#=============================================================================#
#       P R E P A R E   V A R I A B L E S                                     #
#=============================================================================#

# params[symb+period, arg1, arg2, ..]
params = get_parameters()
limit = 2000
batch_size = 64
fit_epoch = 100
gru1 = 16
gru2 = 8
run_type = 0
graph = False

idx = 0
for item in params:
    if idx > 0:
        if item == '-train':
            run_type = 0
        elif item == '-predict':
            run_type = 1
        elif item == '-graph':
            graph = True
        elif item == '-limit':
            pass
        elif int(item) > 0:
            if params[idx-1] == '-train':
                fit_epoch = int(item)
            elif params[idx-1] == '-limit':
                limit = int(item)
    idx += 1

np.random.seed(23)

workfile = params[0]
path = 'C:/Program Files (x86)/STForex MetaTrader 4/MQL4/Files/ML-Assistant/'
file_x = path + workfile + '_x.csv'
file_y = path + workfile + '_y.csv'
file_xx = path + workfile + '_xx.csv'
file_yy = path + workfile + '_yy.csv'
prefix = 'C:/mas/simple_rnn_bin_'
model = None
data_x = np.array([])
data_y = np.array([])
train_x = np.array([])
train_y = np.array([])
test_x = np.array([])
test_y = np.array([])
history = None

# print('Backend:', backend())
print('Work file:', workfile)


#=============================================================================#
#       L O A D   D A T A                                                     #
#=============================================================================#
if run_type == 0:
    print('\nPrepare Data...')
    data_x = np.genfromtxt(file_x, delimiter=';')
    data_y = np.genfromtxt(file_y, delimiter=';')
    # batch_input_shape=( batch_size, timesteps, units )
    data_x = np.reshape(data_x, (data_x.shape[0], 1, data_x.shape[1]))
#    data_y = signal_to_class(data_yt)

    start, size = 0, len(data_x)
    if size > limit:
        start = size - limit
        size = limit
    train_size = int(size * 0.65)
    test_size = size - train_size
    train_x, test_x = data_x[start:start+train_size, :], data_x[start+train_size:len(data_x), :]
    train_y, test_y = data_y[start:start+train_size], data_y[start+train_size:len(data_y)]
    print('Train/Test :', len(train_y), '/', len(test_y))
#    print(train_y)
#    plt.plot(test_y)
#    plt.show()


#=============================================================================#
#       P R E P A R E   M O D E L                                             #
#=============================================================================#
if run_type == 0:
    print('\nCreating Model...')
    model = Sequential()
    model.add(BatchNormalization(batch_input_shape=(None, 1, data_x.shape[2])))
    model.add(GRU(gru1,
                  activation='relu', 
                  return_sequences=True,
#                  batch_input_shape=(None, 1, data_x.shape[2])))
                  activity_regularizer=regularizers.l2(0.01))) # , batch_input_shape=(None, data_x.shape[1], 1)
#    model.add(LeakyReLU())
#    model.add(Dropout(0.5))
    model.add(GRU(gru2,
                  activation='relu', 
                  activity_regularizer=regularizers.l2(0.01)))
#    model.add(LeakyReLU())
    model.add(Dense(1, activation='tanh'))#softsign, tanh
    save_model(model, prefix + workfile)
elif run_type == 1:
    model = load_model(prefix + workfile)

opt = Nadam(lr=0.01) # Nadam(lr=0.001), RMSprop(), Adam(), SGD()
# loss='hinge', 'squared_hinge', 'categorical_crossentropy'(softmax), 'binary_crossentropy'
model.compile(loss='poisson', optimizer=opt, metrics=['acc'])


#=============================================================================#
#       T R A I N I N G                                                       #
#=============================================================================#
if run_type == 0:
    reduce_lr = ReduceLROnPlateau(factor=0.9, patience=5, min_lr=0.000001, verbose=1) # factor=0.9, patience=5, min_lr=0.000001, verbose=1
    print('\nTraining...')
    history = model.fit(train_x, train_y, #train_x, train_y, data_x, data_y,
                        batch_size=batch_size,
                        epochs=fit_epoch,
                        callbacks=[reduce_lr],
                        validation_data=(test_x, test_y))
    model.save_weights(prefix+workfile+'.hdf5')


#=============================================================================#
#       P R E D I C T I N G                                                   #
#=============================================================================#
print('\nPredicting...')
data_xx = np.genfromtxt(file_xx, delimiter=';')
data_xx = np.reshape(data_xx, (data_xx.shape[0], 1, data_xx.shape[1]))

if run_type == 1:
    model.load_weights(prefix+workfile+'.hdf5')

predicted_output = model.predict(data_xx, batch_size=batch_size)
#data_yy = class_to_signal(predicted_output)
data_yy = predicted_output

np.savetxt(file_yy, data_yy, fmt='%.6f', delimiter=';')
print("Predict saved:\n", file_yy)

if run_type == 0:
    # calculate root mean squared error
    train_predict = model.predict(train_x)
    test_predict = model.predict(test_x)
    train_score = math.sqrt(mean_squared_error(train_y, train_predict))
    print('Train Score: %.6f RMSE' % (train_score))
    test_score = math.sqrt(mean_squared_error(test_y, test_predict))
    print('Test Score: %.6f RMSE' % (test_score))

#=============================================================================#
#       P L O T                                                               #
#=============================================================================#
if graph:
    plt.plot(data_yy)
    plt.title('Predicted')
    plt.ylabel('direction')
    plt.xlabel('bar')
    plt.show()

#    plt.plot(predicted_output)
#    plt.title('Predicted')
#    plt.ylabel('direction')
#    plt.xlabel('bar')
#    plt.show()

    if run_type == 0:
        plt.figure()
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('Model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='best')
        plt.show()

        plt.figure()
        plt.plot(history.history['acc'])
        plt.plot(history.history['val_acc'])
        plt.title('Model accuracy')
        plt.ylabel('acc')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='best')
        plt.show()
