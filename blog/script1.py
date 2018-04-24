# Импортируем основные модули
import sys
import numpy as np

from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import Dense, BatchNormalization
from keras.layers import LeakyReLU
from keras.optimizers import RMSprop, SGD
from keras.optimizers import Adam, Nadam

# Достанем параметры запуска скрипта
parameters = sys.argv

# 
path_to_mql = 'C:/Users/Alexey/AppData/Roaming/MetaQuotes/Terminal/287469DEA9630EA94D0715D755974F1B/MQL4/Files/ML-Assistant/'
symbol = parameters[1]
file_x = path_to_mql + symbol + '_x.csv'
file_y = path_to_mql + symbol + '_y.csv'

#
data_x = np.genfromtxt(file_x, delimiter=';')
data_y = np.genfromtxt(file_y, delimiter=';')

train_x, test_x, train_y, test_y = train_test_split(data_x, data_y, test_size=0.2)
print('Features :', data_x.shape[1])
print('Target :')
print('Train/Test :', len(train_y), '/', len(test_y))

model = Sequential()
model.add(BatchNormalization(batch_input_shape=(None, data_x.shape[1])))
model.add(Dense(32))
model.add(LeakyReLU())
model.add(Dense(32))
model.add(LeakyReLU())
model.add(Dense(32))
model.add(LeakyReLU())
model.add(Dense(32))

