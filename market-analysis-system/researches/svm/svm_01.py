import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
# %matplotlib inline

from sklearn import svm

import sys
sys.path.append('E:\Projects\market-analysis-system\market-analysis-system')
from mas.data import dataset_to_traintest
from mas.data import get_delta
from mas.data import get_diff, get_log_diff, get_sigmoid_to_zero
from mas.classes import signal_to_class, class_to_signal


limit = 5000
path = 'C:/Users/Alexey/AppData/Roaming/MetaQuotes/Terminal/287469DEA9630EA94D0715D755974F1B/MQL4/Files/ML-Assistant/'
workfile = 'EURUSD15'
file_x = path + workfile + '_x.csv'
file_y = path + workfile + '_y.csv'

train_data = np.genfromtxt(file_x, delimiter=';')
target_data = np.genfromtxt(file_y, delimiter=';')
train_data, target_data = train_data[-limit:,1::1], target_data[-limit:]

# data_y = signal_to_class(target_data, n=3, normalize=False)

trainX, testX = dataset_to_traintest(train_data, ratio=0.8)
trainY, testY = dataset_to_traintest(target_data, ratio=0.8)

#Реализация

support = svm.SVR()
support.fit(trainX, trainY)
print('Accuracy: \n', support.score(testX, testY))
pred = support.predict(testX)

#Визуализация

plt.plot(pred[-200:])
plt.plot(testY[-200:])
plt.title('Predict')
plt.ylabel('class')
plt.xlabel('bar')
plt.legend(['prediction', 'real'])
plt.show()

# sns.set_context("notebook", font_scale=1.1)
# sns.set_style("ticks")
# sns.lmplot('X1','X2', scatter=True, fit_reg=False, hue='Y')
# plt.ylabel('X2')
# plt.xlabel('X1')
