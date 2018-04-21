# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
#   Market Analysis System                                                    #
#   https://www.mql5.com/ru/users/terentyev23                                 #
#                                                                             #
#   M A R K E T   A N A L Y S I S   S C R I P T   W I T H   K E R A S         #
#                                                                             #
#   Aleksey Terentew                                                          #
#   terentew.aleksey@ya.ru                                                    #
#                                                                             #
###############################################################################

from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import math
from keras.backend import backend
from keras.models import Sequential
from keras.layers import Dense, GRU, Reshape, Dropout, Activation
from keras.layers import BatchNormalization, LeakyReLU
from keras.callbacks import ReduceLROnPlateau
from keras.optimizers import RMSprop, Adam, SGD, Nadam
from sklearn.metrics import mean_squared_error

#=============================================================================#
batch_size =    64
fit_epoch =     100

gru1 =          64
gru2 =          32

prefix = '052_v2_'
workfile = 'AUDUSD.pro5'
path = 'C:/Program Files (x86)/STForex MetaTrader 4/MQL4/Files/ML-Assistant/'
#=============================================================================#
file_x = path + workfile + '_x.csv'
file_y = path + workfile + '_y.csv'
file_xx = path + workfile + '_xx.csv'
file_yy = path + workfile + '_yy.csv'

np.random.seed(7)

print('Backend =', backend())
print('Symbol =', workfile)
#=============================================================================#
#       L O A D   D A T A                                                     #
#=============================================================================#
print('Prepare Data...')

data_x = np.genfromtxt(file_x, delimiter=';')
data_yt = np.genfromtxt(file_y, delimiter=';')

# batch_input_shape=( batch_size, timesteps, units )
data_x = np.reshape(data_x, (data_x.shape[0], 1, data_x.shape[1]))

print("data_x:", data_x.shape)
print("data_y:", data_yt.shape)

data_y = np.array( [], ndmin=2 )
for item in data_yt:
    if item > 0:
        data_y = np.append( data_y, [abs(item), 0.0] )
    if item < 0:
        data_y = np.append( data_y, [0.0, abs(item)] )
    if item == 0:
        data_y = np.append( data_y, [0.0, 0.0] )

data_y = np.reshape( data_y, (data_yt.shape[0], 2) )

train_size = int( len(data_x) * 0.8 )
test_size = len(data_x) - train_size
train_x, test_x = data_x[0:train_size,:], data_x[train_size:len(data_x),:]
print( len(train_x), len(test_x) )
train_y, test_y = data_y[0:train_size,:], data_y[train_size:len(data_y),:]
print( len(train_y), len(test_y) )


#=============================================================================#
#       P R E P A R E   M O D E L                                             #
#=============================================================================#
print( '\nCreating or Load Model...' )

model = Sequential()
model.add( BatchNormalization( batch_input_shape=( None, 1, data_x.shape[2] ) ) )
model.add( GRU( gru1 ) )
model.add( Dropout(0.5) )
model.add( Reshape( (1, gru1) ) )
model.add( GRU( gru2 ) )
model.add( Dense(2) )
model.add( Activation('softmax') )

opt = Nadam(lr=0.001)
reduce_lr = ReduceLROnPlateau( monitor='val_loss', factor=0.9, patience=5, min_lr=0.000001, verbose=1 )

# loss='mse', 'msle', 'categorical_crossentropy'(softmax)
# optimizer='adam', 'rmsprop', opt
model.compile( loss='categorical_crossentropy', optimizer=opt, metrics=['acc'] )


#=============================================================================#
#       T R A I N I N G                                                       #
#=============================================================================#
print( '\nTraining...' )

history = model.fit(train_x, train_y, #train_x, train_y, data_x, data_y, 
                    batch_size=batch_size,
                    epochs=fit_epoch,
                    validation_data=( test_x, test_y ),
                    callbacks=[reduce_lr])


#=============================================================================#
#       P R E D I C T I N G                                                   #
#=============================================================================#
print( '\nPredicting...' )

data_xx = np.genfromtxt( file_xx, delimiter=';' )
data_xx = np.reshape( data_xx, (data_xx.shape[0], 1, data_xx.shape[1]) )

print( "data_xx:", data_xx.shape )

predicted_output = model.predict( data_xx, batch_size=batch_size )

data_yy = np.array( [] )
for item in predicted_output:
    data_yy = np.append( data_yy, item[0] - item[1] ) #item[0] - item[1]

np.savetxt( file_yy, data_yy, fmt='%.6f', delimiter=';' )

print( "Predict saved:", file_yy )

# make predictions
trainPredict = model.predict( train_x )
testPredict = model.predict( test_x )
# calculate root mean squared error
trainScore = math.sqrt( mean_squared_error( train_y, trainPredict ) )
print( 'Train Score: %.6f RMSE' % ( trainScore ) )
testScore = math.sqrt( mean_squared_error( test_y, testPredict ) )
print( 'Test Score: %.6f RMSE' % ( testScore ) )


#=============================================================================#
#       Plot                                                                  #
#=============================================================================#
plt.plot( data_yy )
plt.title('Predicted')
plt.ylabel('direction')
plt.xlabel('bar')
plt.show()

plt.plot( predicted_output )
plt.title( 'Predicted' )
plt.ylabel( 'direction')
plt.xlabel( 'bar')
plt.show()


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

