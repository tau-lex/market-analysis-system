# Импортируем основные модули
import sys
import numpy as np


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

train_x, test_x, train_y, test_y = 


