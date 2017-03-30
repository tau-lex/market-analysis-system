# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
#   Market Analysis System                                                    #
#   https://www.mql5.com/ru/users/terentjew23                                 #
#                                                                             #
#   M A R K E T   A N A L Y S I S   S C R I P T   W I T H   K E R A S         #
#                                                                             #
#   Aleksey Terentew                                                          #
#   terentew.aleksey@ya.ru                                                    #
#                                                                             #
###############################################################################

from __future__ import print_function
import numpy as np
from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Dense, GRU, Reshape
#import matplotlib.pyplot as plt


batch_size =    26
nb_epoch =      10
epochs =        10

workfile = 'NZDUSD.pro60'
path = 'C:/Program Files (x86)/STForex MetaTrader 4/MQL4/Files/TS_ML/'
                         
file_x = path + workfile + '_x.csv'
file_y = path + workfile + '_y.csv'
file_xx = path + workfile + '_xx.csv'
file_yy = path + workfile + '_yy.csv'

#=============================================================================#
print('   Prepare Data...' )

data_x = np.genfromtxt(file_x, delimiter=';')
#data_y = np.genfromtxt('output_data_y.csv', delimiter=',')
data_y = np.genfromtxt(file_y, delimiter=';')

#print( "data_x:", data_x.shape )
#print( "data_y:", data_y.shape )

data_x = np.reshape( data_x, (data_x.shape[0], data_x.shape[1], 1) )
#data_y = np.reshape( data_y, (data_y.shape[0], data_y.shape[1], 1) )

print( "data_x:", data_x.shape )
print( "data_y:", data_y.shape )
#=============================================================================#
print( '   Creating or Load Model..' )

json_string = ''
try:
    f = open( 'mas.model', 'r' )
except IOError as e:
    print( 'Dont opened a file' )
else:
    json_string = f.read()
    f.close()
    
if( len(json_string) > 0 ):
    model = model_from_json( json_string )
    print( 'Model loaded' )
else:
    model = Sequential()
    model.add( GRU( 11, batch_input_shape=(None, 11, 1) ) )
    model.add( Reshape( (11, 1) ) )
    model.add( GRU( 8 ) )
    model.add( Dense( 4 ) )
    model.add( Dense( 1, activation='tanh' ) ) # 'softsign' 'tanh'
    print( 'Model created' )

model.compile( loss='hinge', optimizer='rmsprop', metrics=['accuracy'] )

json_string = model.to_json()
with open( 'mas.model', 'w' ) as f:
    f.write(json_string)
#=============================================================================#
print( '   Training...' )

try:
    model.load_weights( 'weights.hdf5', by_name=False )
except IOError as e:
    print( 'Don\'t opened a weights file. New train.' )
    
for i in range( epochs ):
    print( 'Epoch', i+1, '/', epochs )
    model.fit(data_x,
              data_y,
              batch_size=batch_size,
              verbose=1,
              nb_epoch=nb_epoch,
              shuffle=False)
    
model.save_weights( 'weights.hdf5' )
#    model.reset_states()

#=============================================================================#
print( '   Predicting...' )

data_xx = np.genfromtxt(file_xx, delimiter=';')
data_xx = np.reshape( data_xx, (data_xx.shape[0], data_xx.shape[1], 1) )

print( "data_xx:", data_xx.shape )

predicted_output = model.predict( data_xx, batch_size=1 )

np.savetxt( file_yy, predicted_output, fmt='%f', delimiter=';')

print( "predict:", predicted_output )

#=============================================================================#
#print( '   Plotting Results...' )
#plt.subplot(2, 1, 1)
#plt.plot(expected_output)
#plt.title('Expected')
#plt.subplot(2, 1, 2)
#plt.plot(predicted_output)
#plt.title('Predicted')
#plt.show()



