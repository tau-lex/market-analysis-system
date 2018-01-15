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

#import math
import matplotlib.pyplot as plt
import numpy as np

from mas.data import create_timeseries_matrix, dataset_to_traintest
from mas.data import get_delta, get_deltas_from_ohlc
from mas.data import get_diff, get_sigmoid_to_zero
from mas.models import save_model, load_model

from keras.models import Sequential
from keras.layers import Dense, GRU, Dropout, BatchNormalization
from keras.layers import LeakyReLU#, PReLU
from keras.callbacks import ReduceLROnPlateau
from keras import regularizers

from statsmodels.nonparametric.smoothers_lowess import lowess
#from sklearn.metrics import mean_squared_error


#=============================================================================#
#       P R E P A R E   V A R I A B L E S                                     #
#=============================================================================#
optimizers = ['RMSprop', 'SGD', 'Adagrad', 'Adadelta', 'Adam', 'Adamax', 'Nadam']
losses = ['mse', 'mae', 'mape', 'msle', 'squared_hinge', 'hinge', \
          'kullback_leibler_divergence', 'poisson', 'cosine_proximity', 'binary_crossentropy']
# params[symb+period, arg1, arg2, ..]
params = ['EURUSD.pro1440', '-train', 100, '-graph']
limit = 5000
batch_size = 128
fit_epoch = 100
fit_train_test = 0.75
recurent_1 = 32
recurent_2 = 32
run_type = 0
graph = False

idx = 0
for idx in range(len(params) - 1):
    if idx > 0:
        if params[idx] == '-train':
            run_type = 0
        elif params[idx] == '-predict':
            run_type = 1
        elif params[idx] == '-graph':
            graph = True
        elif params[idx] == '-limit':
            pass
        elif int(params[idx]) > 0:
            if params[idx-1] == '-train':
                fit_epoch = int(params[idx])
            elif params[idx-1] == '-limit':
                limit = int(params[idx])

np.random.seed(23)

# Main
# path = 'C:/Users/Alexey/AppData/Roaming/MetaQuotes/Terminal/E63399EA98C6C836F270F6A0E01167D0/MQL4/Files/ML-Assistant/'
# Server
params[0] = 'EURUSD1440'
path = 'C:/Users/Adminka/AppData/Roaming/MetaQuotes/Terminal/287469DEA9630EA94D0715D755974F1B/MQL4/Files/ML-Assistant/'
workfile = params[0]
prefix = 'mas_research #3(maxdata-regr-regul)/'
research_prefix = ''
file_x = path + workfile + '_x.csv'
file_y = path + workfile + '_y.csv'
file_xx = path + workfile + '_xx.csv'
file_yy = ''

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
    delta_prices = get_deltas_from_ohlc(data, 7)
    derivative1 = get_diff(data[:, 7], 1)
    derivative2 = get_diff(data[:, 8], 1)
    derivative3 = get_diff(data[:, 9], 1)
    derivative4 = get_diff(data[:, 10], 1)
    sigmoid = get_sigmoid_to_zero(data[:, 10])
    _lowess = lowess(data[:, 10], range(data.shape[0]), return_sorted=False)

    delta_ema1 = get_delta(data, 4, 5)
    delta_ema2 = get_delta(data, 6, 7)

    return np.array([data[:, 0], data[:, 1], # time data
                     data[:, 2], data[:, 3], # time data
                     data[:, 4], data[:, 5], # time data
                     data[:, 6], # time data
                     data[:, 7], data[:, 8], # prices data
                     data[:, 9], data[:, 10], # prices data
                     delta_prices[:, 0], delta_prices[:, 1], delta_prices[:, 2],
                     delta_prices[:, 3], delta_prices[:, 4], delta_prices[:, 5],
                     derivative1, derivative2,
                     derivative3, derivative4,
                     sigmoid,
                     _lowess,
                     data[:, 11], data[:, 12], # ema data
                     data[:, 13], data[:, 14], # ema data
                     delta_ema1, delta_ema2,
                     data[:, 15], data[:, 16], # macd
                     data[:, 17], data[:, 18], # atr, cci
                     data[:, 19] # rsi
                    ]).swapaxes(0, 1)
    
if run_type == 0:
    print('Loading Data...')

    train_data = np.genfromtxt(file_x, delimiter=';')
    target_data = np.genfromtxt(file_y, delimiter=';')

    data_x = prepare_data(train_data)
    data_x, data_y = create_timeseries_matrix(data_x, target_data, 3)

    # batch_input_shape=( batch_size, timesteps, units )
    data_x = np.reshape(data_x, (data_x.shape[0], data_x.shape[1], 1))

    train_x, test_x = dataset_to_traintest(data_x, ratio=fit_train_test, limit=limit)
    train_y, test_y = dataset_to_traintest(data_y, ratio=fit_train_test, limit=limit)
    print('Train/Test :', len(train_x), '/', len(test_x))


new_data = np.genfromtxt(file_xx, delimiter=';')
data_xx = prepare_data(new_data)
data_xx, empty = create_timeseries_matrix(data_xx, look_back=3)
data_xx = np.reshape(data_xx, (data_xx.shape[0], data_xx.shape[1], 1))


#=============================================================================#
#   P R E P A R E  ->  T R A I N I N G  ->  P R E D I C T I N G  ->  P L O T  #
#=============================================================================#
if run_type == 0:
    for optimizer in optimizers:
        for loss in losses:
            print('Creating Model...')

            model = Sequential()
            model.add(BatchNormalization(batch_input_shape=(None, data_x.shape[1], data_x.shape[2])))
            model.add(GRU(recurent_1,
                           return_sequences=True,
                           # bias_initializer='ones',
                           activity_regularizer=regularizers.l2(0.01)
            ))
            model.add(LeakyReLU())
            model.add(Dropout(0.5))
            model.add(GRU(recurent_2,
                           return_sequences=True,
                           activity_regularizer=regularizers.l2(0.01)))
            model.add(LeakyReLU())
            model.add(Dropout(0.4))
            model.add(GRU(recurent_2, activity_regularizer=regularizers.l2(0.01)))
            model.add(LeakyReLU())
            model.add(Dropout(0.3))
            model.add(BatchNormalization())
            model.add(Dense(16))
            model.add(Dense(8))
            model.add(Dense(1))

            research_prefix = optimizer + '-' + loss + '_'
            save_model(model, prefix + research_prefix + workfile + '.model')

            model.compile(loss=loss, optimizer=optimizer, metrics=['acc'])

            print('\nTraining...')

            reduce_lr = ReduceLROnPlateau(factor=0.5, patience=10, min_lr=0.0001, verbose=1)

            history = model.fit(train_x, train_y, #train_x, train_y, data_x, data_y,
                                batch_size=batch_size,
                                epochs=fit_epoch,
                                callbacks=[reduce_lr],
                                validation_data=(test_x, test_y))

            # save_model(model, prefix + research_prefix + workfile + '.model')
            model.save_weights(prefix + research_prefix + workfile + '.hdf5')

            print('\nPredicting...')

            data_yy = model.predict(data_xx, batch_size=batch_size)

            file_yy = prefix + research_prefix + workfile + '_yy.csv'

            np.savetxt(file_yy, data_yy, fmt='%.6f', delimiter=';')
            print("Predict saved:\n", file_yy)

#            # calculate root mean squared error
#            train_predict = model.predict(train_x)
#            test_predict = model.predict(test_x)
#            train_score = math.sqrt(mean_squared_error(train_y, train_predict))
#            print('Train Score: %.6f RMSE' % (train_score))
#            test_score = math.sqrt(mean_squared_error(test_y, test_predict))
#            print('Test Score: %.6f RMSE' % (test_score))

            print('Save graphs')

            plt.plot(data_yy)
            plt.title('Saved predict | ' + research_prefix)
            plt.ylabel('direction')
            plt.xlabel('bar')
            plt.legend(['prediction'])
#            plt.show()
            plt.savefig(prefix + research_prefix + workfile + '_prediction.png')
            plt.close()

            plt.figure()
            plt.plot(history.history['loss'])
            plt.plot(history.history['val_loss'])
            plt.title('Model loss | ' + research_prefix)
            plt.ylabel('loss')
            plt.xlabel('epoch')
            plt.legend(['train', 'test'], loc='best')
#            plt.show()
            plt.savefig(prefix + research_prefix + workfile + '_loss.png')
            plt.close()

            plt.figure()
            plt.plot(history.history['acc'])
            plt.plot(history.history['val_acc'])
            plt.title('Model accuracy | ' + research_prefix)
            plt.ylabel('acc')
            plt.xlabel('epoch')
            plt.legend(['train', 'test'], loc='best')
#            plt.show()
            plt.savefig(prefix + research_prefix + workfile + '_accuracy.png')
            plt.close()

elif run_type == 1:
    for optimizer in optimizers:
        for loss in losses:
            print('\nPredicting...')

            research_prefix = optimizer + '-' + loss + '_'

            model = load_model(prefix + research_prefix + workfile + '.model')
            model.load_weights(prefix + research_prefix + workfile + '.hdf5')

            data_yy = model.predict(data_xx, batch_size=batch_size)

            np.savetxt(file_yy, data_yy, fmt='%.6f', delimiter=';')
            print("Predict saved:\n", file_yy)

