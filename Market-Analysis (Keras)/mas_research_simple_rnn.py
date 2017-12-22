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
#import math
import matplotlib.pyplot as plt
import numpy as np
from mas_include import create_timeseries_matrix, get_delta
#from mas_include import signal_to_class2, class2_to_signal
#from mas_include import signal_to_class3, class3_to_signal
from mas_include import save_model, load_model
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.layers import BatchNormalization
#from keras.layers import LeakyReLU, PReLU
#from keras.optimizers import RMSprop, SGD
#from keras.optimizers import Adam, Nadam, Adagrad, Adamax, Adadelta
from keras.callbacks import ReduceLROnPlateau
#from keras import regularizers
#from sklearn.metrics import mean_squared_error


#=============================================================================#
#       P R E P A R E   V A R I A B L E S                                     #
#=============================================================================#
optimizers = ['RMSprop', 'SGD', 'Adagrad', 'Adadelta', 'Adam', 'Adamax', 'Nadam']
losses = ['mse', 'mae', 'mape', 'msle', 'squared_hinge', 'hinge', \
          'kullback_leibler_divergence', 'poisson', 'cosine_proximity', 'binary_crossentropy']
# params[symb+period, arg1, arg2, ..]
#params = get_parameters()
params = ['EURUSD.pro1440', '-train', 100, '-graph']
limit = 10000
batch_size = 200
fit_epoch = 100
fit_train_test = 0.8
recurent_1 = 32
recurent_2 = 16
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

prefix = 'mas_research/'
research_prefix = ''
workfile = params[0]
path = 'C:/Program Files (x86)/STForex MetaTrader 4/MQL4/Files/ML-Assistant/'
file_x = path + workfile + '_x.csv'
file_y = path + workfile + '_y.csv'
file_xx = path + workfile + '_xx.csv'
file_yy = workfile + '_yy.csv'

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
    print('Loading Data...')

    train_data = np.genfromtxt(file_x, delimiter=';')
    target_data = np.genfromtxt(file_y, delimiter=';')

    d1 = get_delta(train_data, 0, 3) # Open - Close
    d2 = get_delta(train_data, 1, 0) # High - Open
    d3 = get_delta(train_data, 1, 3) # High - Close
    d4 = get_delta(train_data, 0, 2) # Open - Low
    d5 = get_delta(train_data, 0, 2) # Close - Low
    d6 = get_delta(train_data, 1, 2) # High - Low
    d_ema1 = get_delta(train_data, 4, 5)
    d_ema2 = get_delta(train_data, 6, 7)

    data_x = np.array([d1, d1, d3, d4, d5, d6, d_ema1, d_ema2, train_data[:, 8], train_data[:, 9]])

    data_x, data_y = create_timeseries_matrix(data_x.swapaxes(0, 1), target_data, 3)

    # batch_input_shape=( batch_size, timesteps, units )
    data_x = np.reshape(data_x, (data_x.shape[0], data_x.shape[1], 1))

    start, size = 0, len(data_x)
    if size > limit:
        start, size = size - limit, limit
    train_size = int(size * fit_train_test)
    test_size = size - train_size
    train_x, test_x = data_x[start:start+train_size, :], data_x[start+train_size:len(data_x), :]
    train_y, test_y = data_y[start:start+train_size,], data_y[start+train_size:len(data_y),]
    print('Train/Test :', train_size, '/', test_size)


data_xx = np.genfromtxt(file_xx, delimiter=';')

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
            model.add(BatchNormalization(batch_input_shape=(None, data_x.shape[1], 1)))
            model.add(LSTM(recurent_1,
                           return_sequences=True,
                           # bias_initializer='ones',
                           # activity_regularizer=regularizers.l2(0.01)
            ))
            model.add(Dropout(0.5))
            model.add(LSTM(recurent_2))
            model.add(Dense(8))
            model.add(Dense(1))

            research_prefix = optimizer + '-' + loss + '_'
            save_model(model, prefix + research_prefix + workfile)

            model.compile(loss=loss, optimizer=optimizer, metrics=['acc'])

            print('\nTraining...')

            reduce_lr = ReduceLROnPlateau(factor=0.5, patience=10, min_lr=0.0001, verbose=1)

            history = model.fit(train_x, train_y, #train_x, train_y, data_x, data_y,
                                batch_size=batch_size,
                                epochs=fit_epoch,
                                callbacks=[reduce_lr],
                                validation_data=(test_x, test_y))
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

            model = load_model(prefix + research_prefix + workfile)
            model.load_weights(prefix + research_prefix + workfile + '.hdf5')

            data_yy = model.predict(data_xx, batch_size=batch_size)

            np.savetxt(file_yy, data_yy, fmt='%.6f', delimiter=';')
            print("Predict saved:\n", file_yy)

