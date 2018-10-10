# -*- coding: utf-8 -*-
import math
import matplotlib.pyplot as plt
import numpy as np

from mas_tools.os import get_parameters
from mas_tools.ml import plot_history, classification_scores
from mas_tools.ml import save_model_arch
from mas_tools.data import create_timeseries_matrix
from mas_tools.data import get_delta, get_diff, get_log_diff
from mas_tools.data import get_sigmoid_to_zero, get_sigmoid_ration
from mas_tools.models import save_model, load_model
from mas_tools.classes import signal_to_class, class_to_signal
from sklearn.model_selection import train_test_split

from keras.models import Sequential, Model
from keras.layers import Input, Reshape
from keras.layers import BatchNormalization, concatenate
from keras.layers import Dense, Activation
from keras.layers import LSTM, GRU
from keras.layers import LeakyReLU
from keras.layers import Dropout, ActivityRegularization
from keras.layers.wrappers import Bidirectional
from keras import regularizers
from keras.optimizers import RMSprop, SGD
from keras.optimizers import Adam, Nadam, Adagrad, Adamax, Adadelta
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from keras.callbacks import CSVLogger, EarlyStopping


#=============================================================================#
#       P R E P A R E   V A R I A B L E S                                     #
#=============================================================================#
# params[symb+period, arg1, arg2, ..]
params = ['EURUSD30', '-train', '3', '-graph']
# params = ['EURUSD15', '-predict']
limit = 65000
batch_size = 512
fit_epoch = 100
train_test = 0.1
ts_lookback = 5

nclasses = 2
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
workfile = '_eurusd' #params[0]
file_x = path + workfile + '_x.csv'
file_y = path + workfile + '_y.csv'
file_xx = path + workfile + '_xx.csv'
file_yy = path + workfile + '_yy.csv'
prefix = 'tmp/_tmp_cl_0_'
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
    return data
    # for time(0, 6), market(7, 10), ema(11, 14), macd(15, 16)
    # for atr(17), cci(18), rsi(19), usdx(20), eurx(21)
    #----------------------------
    # for market(0, 3), ema(4, 7),
    # for atr(8), cci(9), rsi(10)
    mrkt, ema = range(4), range(4, 8)
    # delta = get_delta(data, mrkt[0], mrkt[3])
    diff1 = get_diff(data[:, mrkt[1]])
    diff2 = get_diff(data[:, mrkt[2]])
    diff3 = get_diff(data[:, mrkt[3]])
    # logdiff1 = get_log_diff(data[:, mrkt[1]])
    # logdiff2 = get_log_diff(data[:, mrkt[2]])
    # logdiff3 = get_log_diff(data[:, mrkt[3]])
    detrend1 = get_delta(data, mrkt[3], ema[0]) # close - ema13
    detrend2 = get_delta(data, mrkt[3], ema[1]) # close - ema26
    #
    ediff1 = get_diff(data[:, ema[0]])
    ediff2 = get_diff(data[:, ema[1]])
    ediff3 = get_diff(data[:, ema[2]])
    # elogdiff1 = get_log_diff(data[:, 11])
    # elogdiff2 = get_log_diff(data[:, 12])
    # elogdiff3 = get_log_diff(data[:, 13])
    return np.array(np.column_stack((
                            # data[:, 5:6], # hours and minutes
                            # data[:, 8:11], # prices (without open)
                            # delta,
                            diff1, diff2, diff3,
                            # logdiff1, logdiff2, logdiff3,
                            detrend1, detrend2,
                            ediff1, ediff2, ediff3,
                            # elogdiff1, elogdiff2, elogdiff3,
                            # data[:, 15:17], # macd
                            # data[:, 17:19], data[:, 19]-50, # atr, cci, rsi
                            # data[:, 20:22], # usd and eur indexes
                          ))
                    )


print('Loading Data...')

train_data = np.genfromtxt(file_x, delimiter=',')
# target_data = np.genfromtxt(file_y, delimiter=';')

# train_data, target_data = train_data[-limit:,], target_data[-limit:]
# data_x = prepare_data(train_data)
data_x, data_y = train_data[:, :-1], train_data[:, -1]
shape_x = data_x.shape
data_y = signal_to_class(data_y, n=nclasses)
# data_x, data_y = create_timeseries_matrix(data_x, data_y, ts_lookback)

# batch_input_shape=(batch_size, timesteps, units)
# data_x = np.reshape(data_x, (data_x.shape[0], 1, shape_x[1]))

# For training validation
train_x, test_x, train_y, test_y = train_test_split(data_x, data_y, test_size=train_test)
train_x1, train_x2 = np.column_stack((train_x[:, 1:4], train_x[:, 5],
                                train_x[:, 7], train_x[:, 10:16], train_x[:, 24])), \
                     np.column_stack((train_x[:, 4], train_x[:, 6],
                                train_x[:, 8:10], train_x[:, 16:24]))
test_x1, test_x2 = np.column_stack((test_x[:, 1:4], test_x[:, 5],
                                test_x[:, 7], test_x[:, 10:16], test_x[:, 24])), \
                     np.column_stack((test_x[:, 4], test_x[:, 6],
                                test_x[:, 8:10], test_x[:, 16:24]))

print('Input data shape :', data_x.shape)
print('Train/Test :', len(train_y), '/', len(test_y))


#=============================================================================#
#       P R E P A R E   M O D E L                                             #
#=============================================================================#
print('\nCreating Model...')

batch_size = 512
fa = 'elu'
init = 'lecun_uniform' #'lecun_uniform' #'random_normal'
init_b = 'lecun_uniform'
reg = regularizers.l2
rs = 0.001
Rcrnt = LSTM

in_a = Input(shape=(test_x1.shape[1],))
a = BatchNormalization()(in_a)
a = Dense(32, kernel_initializer=init, activation='relu')(a)
a = Reshape((1, 32))(a)
a = Rcrnt(50,
        return_sequences=True,
        activation=fa,
        kernel_initializer=init,
        bias_initializer=init_b,
        kernel_regularizer=reg(rs),
        recurrent_activation='elu',
        recurrent_regularizer=reg(rs)
        )(a)
a = Dropout(0.5)(a)

in_b = Input(shape=(test_x2.shape[1],))
b = BatchNormalization()(in_b)
b = Dense(32, kernel_initializer=init, activation='relu')(b)
b = Reshape((1, 32))(b)
b = Rcrnt(50,
        return_sequences=True,
        activation=fa,
        kernel_initializer=init,
        bias_initializer=init_b,
        kernel_regularizer=reg(rs),
        recurrent_activation='elu',
        recurrent_regularizer=reg(rs)
        )(b)
b = Dropout(0.5)(b)

x = concatenate([a, b])

x = Rcrnt(64,
        activation=fa,
        kernel_initializer=init,
        bias_initializer=init_b,
        # kernel_regularizer=reg(rs),
        recurrent_activation='elu',
        recurrent_regularizer=reg(rs)
        )(x)
x = Dropout(0.5)(x)
x = Dense(16,
        activation=fa,
        kernel_initializer=init,
        bias_initializer=init_b,
        # kernel_regularizer=regularizers.l2(rs)
        )(x)
out = Dense(nclasses,
        activation='softmax',
        kernel_initializer=init,
        bias_initializer=init_b,
        )(x)

model = Model(inputs=[in_a, in_b], outputs=out)

path2 = 'E:/Projects/market-analysis-system/mas_mt/'
save_model(model, path2 + prefix + workfile + '.model')

opt = Nadam(lr=0.008)
model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['categorical_accuracy'])

save_model_arch(model, path2 + 'simple')

#=============================================================================#
#       T R A I N I N G                                                       #
#=============================================================================#
print('Training...')

reduce_lr = ReduceLROnPlateau(factor=0.1, patience=3, min_lr=0.00001, verbose=1)
fn = path2 + prefix + workfile + '_{epoch:02d}-{val_loss:.2f}.hdf5'
checkpointer = ModelCheckpoint(filepath=fn, verbose=0, save_best_only=True)
es = EarlyStopping(patience=20, min_delta=0.001)

history = model.fit([train_x1, train_x2], train_y,
                    batch_size=batch_size,
                    epochs=fit_epoch,
                    shuffle=True,
                    callbacks=[reduce_lr],
                    validation_data=([test_x1, test_x2], test_y)
                    )

model.save_weights(path2 + prefix + workfile + '.hdf5')


#=============================================================================#
#       P R E D I C T I N G                                                   #
#=============================================================================#
print('\nPredicting...')

test_data = np.genfromtxt(file_xx, delimiter=',')
test_xx, data_yyy = test_data[:, :-1], test_data[:, -1]
# shape_xx = data_xx.shape
# data_xx, empty = create_timeseries_matrix(data_xx, look_back=ts_lookback)
# print(data_xx.shape)
# data_xx = np.reshape(data_xx, (data_xx.shape[0], 1, shape_xx[1]))
# print(data_xx.shape)

test_xx1, test_xx2 = np.column_stack((test_xx[:, 1:4], test_xx[:, 5],
                                test_xx[:, 7], test_xx[:, 10:16], test_xx[:, 24])), \
                     np.column_stack((test_xx[:, 4], test_xx[:, 6],
                                test_xx[:, 8:10], test_xx[:, 16:24]))

if run_type == 1:
    model.load_weights(prefix + workfile + '.hdf5')

# Prediction model
data_yy = model.predict([test_xx1, test_xx2])
predicted = data_yy
data_yy = class_to_signal(data_yy.reshape(test_xx.shape[0], nclasses),
                          n=nclasses,
                          normalized=normalize_class)

np.savetxt(file_yy, data_yy, fmt='%.2f', delimiter=',')
print("Predict saved:\n", file_yy)


#=============================================================================#
#       P L O T                                                               #
#=============================================================================#
# test_y_ = [np.argmax(x) for x in test_y]
# test_yy = [np.argmax(x) for x in model.predict(test_x).reshape(test_x.shape[0], nclasses)]

# true, test
print(classification_scores(data_yyy, data_yy, nclasses))

# plt.plot(predicted)
# plt.title('Predict')
# plt.ylabel('class')
# plt.xlabel('bar')
# plt.legend(['buy', 'hold', 'sell'])
# plt.show()

plt.plot(data_yy)
plt.title('Saved predict')
plt.ylabel('class')
plt.xlabel('bar')
plt.legend(['prediction'])
plt.show()

plot_history(history, acc='categorical_accuracy')

