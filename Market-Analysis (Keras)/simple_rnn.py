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
from mas_include import get_parameters, create_timeseries_matrix
#from mas_include import signal_to_class2, class2_to_signal
#from mas_include import signal_to_class3, class3_to_signal
from mas_include import save_model, load_model
from keras.models import Sequential
from keras.layers import Dense, GRU, LSTM, Dropout, Activation
from keras.layers import BatchNormalization
from keras.layers import LeakyReLU, PReLU
from keras.optimizers import RMSprop, SGD
from keras.optimizers import Adam, Nadam, Adagrad, Adamax, Adadelta
from keras.callbacks import ReduceLROnPlateau
from keras import regularizers
from sklearn.metrics import mean_squared_error


#=============================================================================#
#       P R E P A R E   V A R I A B L E S                                     #
#=============================================================================#
# params[symb+period, arg1, arg2, ..]
params = get_parameters()
#params = ['EURUSD.pro1440', '-train', 100, '-graph']
limit = 5000
batch_size = 64
fit_epoch = 100
recurent_1 = 32
recurent_2 = 16
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

np.random.seed(7)

workfile = params[0]
path = 'C:/Program Files (x86)/STForex MetaTrader 4/MQL4/Files/ML-Assistant/'
file_x = path + workfile + '_x.csv'
file_y = path + workfile + '_y.csv'
file_xx = path + workfile + '_xx.csv'
file_yy = path + workfile + '_yy.csv'
prefix = 'simple_rnn_'
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
    print('\nLoading Data...')

    data_x = np.genfromtxt(file_x, delimiter=';')
    data_y = np.genfromtxt(file_y, delimiter=';')

    data_x, data_y = create_timeseries_matrix(data_x, data_y, 3)
#    data_y = signal_to_class2(data_yt)

    # batch_input_shape=( batch_size, timesteps, units )
    data_x = np.reshape(data_x, (data_x.shape[0], data_x.shape[1], 1))

    start, size = 0, len(data_x)
    if size > limit:
        start, size = size - limit, limit
    train_size = int(size * 0.8)
    test_size = size - train_size
    train_x, test_x = data_x[start:start+train_size, :], data_x[start+train_size:len(data_x), :]
    train_y, test_y = data_y[start:start+train_size,], data_y[start+train_size:len(data_y),]
    print('Train/Test :', train_size, '/', test_size)


#=============================================================================#
#       P L O T   D A T A                                                     #
#=============================================================================#
#    print(train_y)
#    plt.plot(test_y)
#    plt.show()


#=============================================================================#
#       P R E P A R E   M O D E L                                             #
#=============================================================================#
if run_type == 0:
    print('\nCreating Model...')

    model = Sequential()
    model.add(BatchNormalization(batch_input_shape=(None, data_x.shape[1], 1)))
    model.add(LSTM(recurent_1,
                    # batch_input_shape=(None, data_x.shape[1], 1),
                    # activation='relu',
                    return_sequences=True,
                    # bias_initializer='ones',
                    # activity_regularizer=regularizers.l2(0.01)
    ))
    model.add(LeakyReLU())
    model.add(Dropout(0.5))
    model.add(LSTM(recurent_2,
                    # activation='relu',
                    # bias_initializer='ones',
                    # activity_regularizer=regularizers.l2(0.01)
    ))
#    model.add(PReLU())
    model.add(LeakyReLU())
# 'elu', 'selu', 'relu'
# 'softplus', 'softsign', 'tanh'
# 'sigmoid', 'hard_sigmoid', 'linear' #, activation='sigmoid'
    model.add(Dense(8))
    model.add(Dense(1))

    save_model(model, prefix + workfile)
elif run_type == 1:
    model = load_model(prefix + workfile)

# RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)
# SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=False)
# Adagrad(lr=0.01, epsilon=1e-08, decay=0.0)
# Adadelta(lr=1.0, rho=0.95, epsilon=1e-08, decay=0.0)
# Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
# Adamax(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
# Nadam(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08, schedule_decay=0.004)
# (clipnorm=1.0, clipvalue=1.0)
opt = Nadam()
# 'mse', 'mae', 'mape', 'msle'
# 'squared_hinge', 'hinge', 'kullback_leibler_divergence(kld)'
# 'poisson', 'cosine_proximity'
# 'binary_crossentropy', 'categorical_crossentropy'(softmax)
model.compile(loss='hinge', optimizer=opt, metrics=['acc'])


#=============================================================================#
#       T R A I N I N G                                                       #
#=============================================================================#
if run_type == 0:
    print('\nTraining...')

#   ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=8, verbose=0, mode='auto', epsilon=0.0001, cooldown=0, min_lr=0)
    reduce_lr = ReduceLROnPlateau(factor=0.5, patience=10, min_lr=0.0001, verbose=1)

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

data_xx, empty = create_timeseries_matrix(data_xx, look_back=3)

data_xx = np.reshape(data_xx, (data_xx.shape[0], data_xx.shape[1], 1))


if run_type == 1:
    model.load_weights(prefix+workfile+'.hdf5')

predicted_output = model.predict(data_xx, batch_size=batch_size)
data_yy = predicted_output
#data_yy = class2_to_signal(predicted_output)

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
    plt.title('Saved predict')
    plt.ylabel('direction')
    plt.xlabel('bar')
    plt.legend(['prediction'])
    plt.show()

    plt.plot(predicted_output)
    plt.title('Predicted')
    plt.ylabel('direction')
    plt.xlabel('bar')
    plt.legend(['buy', 'sell'], loc='best')
    plt.show()

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
