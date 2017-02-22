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
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, LSTM

# since we are using stateful rnn tsteps can be set to 1
tsteps = 1
batch_size = 25
epochs = 25

#=============================================================================#
print('Prepare Data')


#=============================================================================#
print('Creating Model')

model = Sequential()

model.add(LSTM(50, batch_input_shape=(50, tsteps, 1), return_sequences=True, stateful=True))
model.add(LSTM(50, return_sequences=False, stateful=True))
model.add(Dense(1))

model.compile(loss='mse', optimizer='rmsprop')

#=============================================================================#
print('Training')
for i in range(epochs):
    print('Epoch', i, '/', epochs)
    model.fit(cos,
              expected_output,
              batch_size=batch_size,
              verbose=1,
              nb_epoch=1,
              shuffle=False)
    model.reset_states()

print('Predicting')
predicted_output = model.predict(cos, batch_size=batch_size)

print('Plotting Results')
plt.subplot(2, 1, 1)
plt.plot(expected_output)
plt.title('Expected')
plt.subplot(2, 1, 2)
plt.plot(predicted_output)
plt.title('Predicted')
plt.show()