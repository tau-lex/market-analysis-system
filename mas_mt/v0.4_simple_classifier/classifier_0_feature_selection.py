# -*- coding: utf-8 -*-
import math
import matplotlib.pyplot as plt
import numpy as np

from mas_tools.os import get_parameters
from mas_tools.ml import plot_history
from mas_tools.data import create_timeseries_matrix
from mas_tools.data import get_delta, get_diff, get_log_diff
from mas_tools.data import get_sigmoid_to_zero, get_sigmoid_ration
from mas_tools.models import save_model, load_model
from mas_tools.classes import signal_to_class, class_to_signal
from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import BatchNormalization
from keras.layers import Dense, Activation
from keras.layers import LeakyReLU
from keras.layers import Dropout, ActivityRegularization
from keras import regularizers
from keras.optimizers import RMSprop, SGD
from keras.optimizers import Adam, Nadam, Adagrad, Adamax, Adadelta
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from keras.callbacks import CSVLogger, EarlyStopping

from sklearn.metrics import mean_squared_error
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import matthews_corrcoef


#=============================================================================#
#       P R E P A R E   V A R I A B L E S                                     #
#=============================================================================#
# params[symb+period, arg1, arg2, ..]
params = ['EURUSD15', '-train', '100', '-graph']
# params = ['EURUSD15', '-predict']
limit = 8000
batch_size = 256
fit_epoch = 100
train_test = 0.2
ts_lookback = 12

nclasses = 3
normalize_class = True

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


path = 'C:/Users/Alexey/AppData/Roaming/MetaQuotes/Terminal/287469DEA9630EA94D0715D755974F1B/MQL4/Files/ML-Assistant/'
workfile = params[0]
file_x = path + workfile + '_x.csv'
file_y = path + workfile + '_y.csv'
file_xx = path + workfile + '_xx.csv'
file_yy = path + workfile + '_yy.csv'
prefix = 'tmp/classifier_0_'
model = None
data_x = np.array([])
data_y = np.array([])
train_x = np.array([])
train_y = np.array([])
test_x = np.array([])
test_y = np.array([])
history = None

# print('Backend:', backend())
print('\nWork file:', workfile)


#=============================================================================#
#       L O A D   D A T A                                                     #
#=============================================================================#
def prepare_data(data):
    # for time(0, 6), market(7, 10), ema(11, 14), macd(15, 16)
    # for atr(17), cci(18), rsi(19), usdx(20), eurx(21)
    #
    delta = get_delta(data, 7, 10)
    # diff1 = get_diff(data[:, 8])
    # diff2 = get_diff(data[:, 9])
    # diff3 = get_diff(data[:, 10])
    logdiff1 = get_log_diff(data[:, 8])
    logdiff2 = get_log_diff(data[:, 9])
    logdiff3 = get_log_diff(data[:, 10])
    detrend1 = get_delta(data, 10, 11) # close - ema13
    detrend2 = get_delta(data, 10, 12) # close - ema26
    #
    # ediff1 = get_diff(data[:, 11])
    # ediff2 = get_diff(data[:, 12])
    # ediff3 = get_diff(data[:, 13])
    elogdiff1 = get_log_diff(data[:, 11])
    elogdiff2 = get_log_diff(data[:, 12])
    elogdiff3 = get_log_diff(data[:, 13])
    #
    # xdiff1 = get_diff(data[:, 20])
    # xdiff2 = get_diff(data[:, 21])
    return np.array(np.column_stack((
                            # data[:, 5:6], # hours and minutes
                            # data[:, 8:11], # prices (without open)
                            delta,
                            # diff1, diff2, diff3,
                            # logdiff1, logdiff2, logdiff3,
                            detrend1, detrend2,
                            # ediff1, ediff2, ediff3,
                            # elogdiff1, elogdiff2, elogdiff3,
                            # data[:, 15:17], # macd
                            data[:, 17:19], data[:, 19]-50, # atr, cci, rsi
                            # data[:, 20:22], # usd and eur indexes
                            # xdelta,
                            # xdiff1, xdiff2,
                            # xlogdiff1, xlogdiff2,
                          ))
                    )

if run_type == 0:
    print('Loading Data...')

    train_data = np.genfromtxt(file_x, delimiter=';')
    target_data = np.genfromtxt(file_y, delimiter=';')

    # train_data, target_data = train_data[-limit:,], target_data[-limit:]

    data_x = prepare_data(train_data)
    shape_x = data_x.shape
    data_y = signal_to_class(target_data, n=nclasses, normalize=normalize_class)
    # data_x, data_y = create_timeseries_matrix(train_data, data_y, ts_lookback)

    # batch_input_shape=(batch_size, timesteps, units)
    # data_x = np.reshape(data_x, (shape_x[0], ts_lookback, shape_x[1]))

    # For training validation
    train_x, test_x, train_y, test_y = train_test_split(data_x, data_y, test_size=train_test)
    
    print('Input data shape :', data_x.shape)
    print('Train/Test :', len(train_y), '/', len(test_y))


#=============================================================================#
#       P R E P A R E   M O D E L                                             #
#=============================================================================#
if run_type == 0:
    print('\nCreating Model...')

    batch_size = 256
    fa = 'tanh'
    init = 'lecun_normal' #'lecun_uniform' #'random_uniform'
    init_b = 'random_uniform'
    reg = regularizers.l2
    rs = 0.01

    model = Sequential()
    model.add(BatchNormalization(batch_input_shape=(None, data_x.shape[1])))
    model.add(Dense(32, 
                    # activation=fa,
                    # kernel_initializer=init,
                    # bias_initializer=init_b,
                    # kernel_regularizer=reg(rs)
                    ))
    model.add(LeakyReLU())
    model.add(Dense(32, 
                    # activation=fa,
                    # kernel_initializer=init,
                    # bias_initializer=init_b,
                    # kernel_regularizer=reg(rs)
                    ))
    model.add(LeakyReLU())
    # model.add(ActivityRegularization(l1=0.01, l2=0.01))
    # model.add(Dropout(0.3))
    model.add(Dense(32, 
                    # activation=fa,
                    # kernel_initializer=init,
                    # bias_initializer=init_b,
                    # kernel_regularizer=reg(rs)
                    ))
    model.add(LeakyReLU())
    model.add(Dense(nclasses,
                    activation='softmax',
                    # kernel_initializer='lecun_uniform',
                    # bias_initializer=init_b,
                    # kernel_regularizer=regularizers.l2(rs)
                    ))

    save_model(model, prefix + workfile + '.model')
elif run_type == 1:
    model = load_model(prefix + workfile + '.model')

# opt = SGD(lr=0.1, momentum=0.0, nesterov=True)
# opt = RMSprop(lr=0.001)
opt = Nadam(lr=0.002)
model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])


#=============================================================================#
#       T R A I N I N G                                                       #
#=============================================================================#
if run_type == 0:
    print('Training...')

    reduce_lr = ReduceLROnPlateau(factor=0.05, patience=5, min_lr=0.000001, verbose=1)
    # checkpointer = ModelCheckpoint(filepath=(prefix+workfile+"_{epoch:02d}-{val_loss:.2f}"+'.hdf5'), verbose=0, save_best_only=True)
    # es = EarlyStopping(patience=40, min_delta=0.0001)

    history = model.fit(train_x, train_y,
                        batch_size=batch_size,
                        epochs=fit_epoch,
                        # callbacks=[reduce_lr],
                        validation_data=(test_x, test_y)
                       )

    model.save_weights(prefix + workfile + '.hdf5')


#=============================================================================#
#       P R E D I C T I N G                                                   #
#=============================================================================#
print('\nPredicting...')

data_xx = prepare_data(np.genfromtxt(file_xx, delimiter=';'))
shape_xx = data_xx.shape
print(data_xx.shape)
# data_xx, empty = create_timeseries_matrix(data_xx, look_back=ts_lookback)
# print(data_xx.shape)
# data_xx = np.reshape(data_xx, (shape_xx[0], ts_lookback, shape_xx[1]))
# print(data_xx.shape)

if run_type == 1:
    model.load_weights(prefix + workfile + '.hdf5')

# Prediction model
data_yy = model.predict(data_xx, batch_size=batch_size)
predicted = data_yy
data_yy = class_to_signal(data_yy.reshape(data_xx.shape[0], nclasses),
                           n=nclasses,
                           normalized=normalize_class)

np.savetxt(file_yy, data_yy, fmt='%.2f', delimiter=';')
print("Predict saved:\n", file_yy)


#=============================================================================#
#       P L O T                                                               #
#=============================================================================#
if graph:
    test_y = class_to_signal(test_y,
                               n=nclasses,
                               normalized=normalize_class)
    test_yy = class_to_signal(model.predict(test_x).reshape(test_x.shape[0], nclasses),
                                       n=nclasses,
                                       normalized=normalize_class)

    print('-' * 20)
    print('\nMATTHEWS CORRELATION')
    print(matthews_corrcoef(test_y, test_yy))
    CM = confusion_matrix(test_y, test_yy, labels=[1, 0, -1])
    print('\nCONFUSION MATRIX')
    print(CM / CM.astype(np.float).sum(axis=1))
    print('\nCLASSIFICATION REPORT')
    print(classification_report(test_y, test_yy, labels=[1, 0, -1], target_names=['buy', 'hold', 'sell']))
    print('-' * 20)

    plt.plot(predicted)
    plt.title('Predict')
    plt.ylabel('class')
    plt.xlabel('bar')
    plt.legend(['buy', 'hold', 'sell'])
    plt.show()

    plt.plot(data_yy)
    plt.title('Saved predict')
    plt.ylabel('class')
    plt.xlabel('bar')
    plt.legend(['prediction'])
    plt.show()

    if run_type == 0:
        plot_history(history)

