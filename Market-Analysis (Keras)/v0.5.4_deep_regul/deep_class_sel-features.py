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

import math
import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.append('E:\Projects\market-analysis-system\Market-Analysis (Keras)')
from mas.include import get_parameters
from mas.data import create_timeseries_matrix, dataset_to_traintest
from mas.data import get_delta
from mas.data import get_diff, get_log_diff, get_sigmoid_to_zero
from mas.models import save_model, load_model
from statsmodels.nonparametric.smoothers_lowess import lowess
from mas.classes import signal_to_class2, class2_to_signal

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
# params = ['EURUSD60', '-train', 100]
limit = 8000
batch_size = 128
fit_epoch = 100
fit_train_test = 0.8
ts_lookback = 10
recurent_1 = 128
recurent_2 = 64
nclasses = 2
normalize_class = False
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

np.random.seed(13)


# Main
path = 'C:/Users/Alexey/AppData/Roaming/MetaQuotes/Terminal/287469DEA9630EA94D0715D755974F1B/MQL4/Files/ML-Assistant/'
# Server
# path = 'C:/Users/Adminka/AppData/Roaming/MetaQuotes/Terminal/287469DEA9630EA94D0715D755974F1B/MQL4/Files/ML-Assistant/'
workfile = params[0]
file_x = path + workfile + '_x.csv'
file_y = path + workfile + '_y.csv'
file_xx = path + workfile + '_xx.csv'
file_yy = path + workfile + '_yy.csv'
prefix = 'c:/mas/deep_regr_sf_'
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
def prepare_data(data):
    # for market (0, 3), ema (4, 7)
    close = data[:, 3]
    sigm1 = get_sigmoid_to_zero(data[:, 1])
    sigm2 = get_sigmoid_to_zero(data[:, 2])
    sigm3 = get_sigmoid_to_zero(data[:, 3])
    delta_oc = get_delta(data, 0, 3)
    diff1 = get_diff(data[:, 1])
    diff2 = get_diff(data[:, 2])
    diff3 = get_diff(data[:, 3])
    logdiff1 = get_log_diff(data[:, 1])
    logdiff2 = get_log_diff(data[:, 2])
    logdiff3 = get_log_diff(data[:, 3])
    lowess1 = lowess(data[:, 3], range(data.shape[0]), return_sorted=False, frac=1./100)
    lowess2 = lowess(data[:, 3], range(data.shape[0]), return_sorted=False, frac=1./250)
    lowess3 = lowess(data[:, 3], range(data.shape[0]), return_sorted=False, frac=1./250, it=0)
    detrend1 = close - lowess1
    detrend2 = close - lowess2
    detrend3 = close - lowess3
    ema1 = data[:, 4]
    ema2 = data[:, 5]
    diff_ema1 = get_diff(data[:, 4])
    diff_ema2 = get_diff(data[:, 5])

    return np.array([sigm1, sigm2, sigm3, delta_oc,
                     diff1, diff2, diff3,
                     logdiff1, logdiff2, logdiff3,
                     # lowess1, lowess2, lowess3,
                     detrend1, detrend2, detrend3,
                     ema1, ema2, diff_ema1, diff_ema2
                    ]).swapaxes(0, 1)

if run_type == 0:
    print('\nLoading Data...')

    train_data = np.genfromtxt(file_x, delimiter=';')
    target_data = np.genfromtxt(file_y, delimiter=';')

    train_data, target_data = train_data[-limit:,], target_data[-limit:]

    data_x = prepare_data(train_data)
    data_y = signal_to_class2(target_data, normalize=normalize_class)
    data_x, data_y = create_timeseries_matrix(data_x, data_y, ts_lookback)

    # batch_input_shape=(batch_size, timesteps, units)
    data_x = np.reshape(data_x, (data_x.shape[0], 1, data_x.shape[1]))

    # For training validation
    train_x, test_x = dataset_to_traintest(data_x, ratio=fit_train_test, limit=limit)
    train_y, test_y = dataset_to_traintest(data_y, ratio=fit_train_test, limit=limit)
    print('Train/Test :', len(train_y), '/', len(test_y))


#=============================================================================#
#       P R E P A R E   M O D E L                                             #
#=============================================================================#
if run_type == 0:
    print('\nCreating Model...')

    model = Sequential()
    model.add(BatchNormalization(batch_input_shape=(None, data_x.shape[1], data_x.shape[2])))
    model.add(GRU(data_x.shape[2],
                  activation='elu',
                  kernel_initializer='lecun_uniform',
                  return_sequences=True,
                  activity_regularizer=regularizers.l2(0.01),
                  dropout=0.0
                 ))
    model.add(GRU(recurent_1,
                  activation='elu',
                  kernel_initializer='glorot_uniform',
                  return_sequences=True,
                  activity_regularizer=regularizers.l2(0.01),
                  dropout=0.5
                 ))
    model.add(GRU(recurent_2,
                  activation='elu',
                  kernel_initializer='glorot_uniform',
                  activity_regularizer=regularizers.l2(0.01),
                  dropout=0.3
                 ))
    model.add(BatchNormalization())
    model.add(Dropout(0.2))
    model.add(Dense(32, activation='elu'))
    model.add(Dropout(0.2))
    model.add(Dense(16, activation='elu'))
    model.add(Dense(8, activation='elu'))
    model.add(Dense(nclasses, activation='softmax'))

    save_model(model, prefix + workfile + '.model')
elif run_type == 1:
    model = load_model(prefix + workfile + '.model')

opt = Nadam()
model.compile(loss='hinge', optimizer=opt, metrics=['acc'])


#=============================================================================#
#       T R A I N I N G                                                       #
#=============================================================================#
if run_type == 0:
    print('\nTraining...')

    # EarlyStopping, ModelCheckpoint
    reduce_lr = ReduceLROnPlateau(factor=0.9, patience=5, min_lr=0.000001, verbose=1)

    history = model.fit(train_x, train_y,
                        batch_size=batch_size,
                        epochs=fit_epoch,
                        callbacks=[reduce_lr],
                        validation_data=(test_x, test_y)
                       )

    model.save_weights(prefix + workfile + '.hdf5')

    # calculate root mean squared error
    train_predict = model.predict(train_x)
    test_predict = model.predict(test_x)
    train_score = math.sqrt(mean_squared_error(train_y, train_predict))
    print('Train Score: %.6f RMSE' % (train_score))
    test_score = math.sqrt(mean_squared_error(test_y, test_predict))
    print('Test Score: %.6f RMSE' % (test_score))


#=============================================================================#
#       P R E D I C T I N G                                                   #
#=============================================================================#
print('\nPredicting...')

new_data = np.genfromtxt(file_xx, delimiter=';')
data_xx = prepare_data(new_data)
data_xx, empty = create_timeseries_matrix(data_xx, look_back=ts_lookback)
data_xx = np.reshape(data_xx, (data_xx.shape[0], 1, data_xx.shape[1]))

if run_type == 1:
    model.load_weights(prefix + workfile + '.hdf5')

# Prediction model
predicted_output = model.predict(data_xx, batch_size=batch_size)

data_yy = np.array([])
for i in range(ts_lookback-1):
    for j in range(nclasses):
        data_yy = np.append(data_yy, [0.0])

data_yy = np.append(data_yy, predicted_output)
data_yy = class2_to_signal(data_yy.reshape(new_data.shape[0], nclasses), normalized=normalize_class)

np.savetxt(file_yy, data_yy, fmt='%.6f', delimiter=';')
print("Predict saved:\n", file_yy)


#=============================================================================#
#       P L O T                                                               #
#=============================================================================#
if graph:
    plt.plot(predicted_output)
    plt.title('Predicted')
    plt.ylabel('direction')
    plt.xlabel('bar')
    plt.legend(['buy', 'sell'], loc='best')
    plt.show()

    plt.plot(data_yy)
    plt.title('Saved predict')
    plt.ylabel('direction')
    plt.xlabel('bar')
    plt.legend(['prediction'])
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
