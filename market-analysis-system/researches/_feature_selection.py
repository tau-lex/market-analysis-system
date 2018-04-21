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
"""The script uses several methods for selecting parameters and displays the results on the graphs."""

import numpy as np

import sys
sys.path.append('E:\Projects\market-analysis-system\Market-Analysis (Keras)')
from mas.data import get_deltas_from_ohlc, get_delta
from mas.data import get_diff, get_log_diff
from mas.data import get_sigmoid_to_zero

from statsmodels.nonparametric.smoothers_lowess import lowess

from mas.classes import signal_to_class, class_to_signal

import matplotlib.pyplot as plt


#=============================================================================#
#       L O A D   D A T A                                                     #
#=============================================================================#
path = 'C:/Users/Alexey/AppData/Roaming/MetaQuotes/Terminal/287469DEA9630EA94D0715D755974F1B/MQL4/Files/ML-Assistant/'
symbol = 'XAUUSD15'
file_x = path + symbol + '_x.csv'
file_y = path + symbol + '_y.csv'

data = np.genfromtxt(file_x, delimiter=';')
data_out = np.genfromtxt(file_y, delimiter=';')

print('data_x shape: ', data.shape)
print('data_y shape: ', data_out.shape)

limit = 100000

if data.shape[0] > limit:
    data = data[-limit:, :]
    data_out = data_out[-limit:, ]
    #
    print('data_x shape: ', data.shape)
    print('data_y shape: ', data_out.shape)


#=============================================================================#
#       P R E P A R E   D A T A                                               #
#=============================================================================#
"""Time [0, 6]"""
time = data[:, 0:7]
logdiff_time = np.column_stack((get_log_diff(time[:, 5]), get_log_diff(time[:, 6])))
"""Price [7, 10]"""
prices = data[:, 7:11]
delta_prices = get_deltas_from_ohlc(prices)
derivative = np.column_stack((get_diff(data[:, 7], 1), get_diff(data[:, 8], 1),
                                get_diff(data[:, 9], 1), get_diff(data[:, 10], 1)))
logdiff = np.column_stack((get_log_diff(data[:, 7]), get_log_diff(data[:, 8]),
                                get_log_diff(data[:, 9]), get_log_diff(data[:, 10])))
sigmoid = np.column_stack((get_sigmoid_to_zero(data[:, 7]), get_sigmoid_to_zero(data[:, 8]),
                                get_sigmoid_to_zero(data[:, 9]), get_sigmoid_to_zero(data[:, 10])))
lowess = lowess(data[:, 10], range(data.shape[0]), return_sorted=False, frac=1./250, it=0)
detrend_close = [prices[:, 3] - data[:, 11], prices[:, 3] - data[:, 12], prices[:, 3] - lowess]
"""EMAs [11, 14]"""
ema = data[:, 11:15]
delta_ema = np.column_stack((get_delta(ema, 0, 1), get_delta(ema, 2, 3)))
diff_ema = np.column_stack((get_diff(ema[:, 0]), get_diff(ema[:, 1]),
                                get_diff(ema[:, 2]), get_diff(ema[:, 3])))
logdiff_ema = np.column_stack((get_log_diff(ema[:, 0]), get_log_diff(ema[:, 1])))
sigmoid_ema = np.column_stack((get_sigmoid_to_zero(ema[:, 0]), get_sigmoid_to_zero(ema[:, 1])))
"""MACD [15, 16]"""
macd = data[:, 15:17]

data_x = np.column_stack(time, logdiff_time,
                            prices, delta_prices, derivative, logdiff,
                            sigmoid, lowess, detrend_close,
                            ema, delta_ema, diff_ema, logdiff_ema, sigmoid_ema,
                            macd, 
                            data[:, 17], data[:, 18], data[:, 19], # atr, cci, rsi [48, 50]
                            data[:, 20], data[:, 21] # usdx, eurx [51, 52]
                        ).swapaxes(0, 1)

sigmoid_y = get_sigmoid_to_zero(data_out)
data_y = signal_to_class(data_out, n=2)


#=============================================================================#
#       P L O T   D A T A                                                     #
#=============================================================================#
idx_start = -100
idx_stop = -1
# plot prices
plt.plot(data[idx_start:, 8])
plt.plot(data[idx_start:, 9])
plt.plot(data[idx_start:, 10])
plt.legend(['high', 'low', 'close'], loc='best')
plt.show()
# plot deltas
plt.plot(delta_prices[idx_start:, 0])
plt.plot(delta_prices[idx_start:, 1])
plt.plot(delta_prices[idx_start:, 2])
plt.plot(delta_prices[idx_start:, 3])
plt.plot(delta_prices[idx_start:, 4])
plt.plot(delta_prices[idx_start:, 5])
plt.legend(['o-c', 'h-l', 'h-o', 'h-c', 'o-l', 'c-l'], loc='best')
plt.show()
# plot derivatives
plt.plot(derivative1[idx_start:])
plt.plot(derivative2[idx_start:])
plt.plot(derivative3[idx_start:])
plt.plot(derivative4[idx_start:])
plt.legend(['open', 'high', 'low', 'close'], loc='best')
plt.show()
# plot log derivatives
plt.plot(logdiff1[idx_start:])
plt.plot(logdiff2[idx_start:])
plt.plot(logdiff3[idx_start:])
plt.plot(logdiff4[idx_start:])
plt.legend(['open', 'high', 'low', 'close'], loc='best')
plt.show()
# plot sigmoids
plt.plot(sigmoid1[idx_start:])
plt.plot(sigmoid2[idx_start:])
plt.plot(sigmoid3[idx_start:])
plt.plot(sigmoid4[idx_start:])
plt.legend(['open', 'high', 'low', 'close'], loc='best')
plt.show()
# plot lowess
_start, _stop = 2000, 2100
plt.plot(data[_start:_stop, 10])
plt.plot(lowess1[_start:_stop])
plt.plot(lowess2[_start:_stop])
plt.plot(lowess3[_start:_stop])
plt.legend(['close', 'lowess 1/100', 'lowess 1/250', 'lowess 1/250 it=0'], loc='best')
plt.show()
# plot comparison
plt.plot(delta_prices[idx_start:, 0])
plt.plot(derivative4[idx_start:])
plt.plot(logdiff4[idx_start:])
plt.plot(detrend_close1[idx_start:])
plt.plot(detrend_close2[idx_start:])
plt.legend(['delta open-close', 'close derivative 1', 'close log diff', 'close - ema 13', 'close - lowess'], loc='best')
plt.show()
# # plot data y
# sigm_y = sigmoid_y / 10
# plt.plot(sigm_y)
# plt.show()

# plot ema
plt.plot(data[idx_start:, 11])
plt.plot(data[idx_start:, 12])
plt.plot(data[idx_start:, 13])
plt.plot(data[idx_start:, 14])
plt.legend(['13', '26', '65', '130'], loc='best')
plt.show()

# plot macd
plt.plot(data[idx_start:, 15])
plt.plot(data[idx_start:, 16])
plt.legend(['line', 'hist'], loc='best')
plt.show()

# plot atr
plt.plot(data[idx_start:, 17])
plt.show()

# plot cci
plt.plot(data[idx_start:, 18])
plt.show()

# plot rsi
plt.plot(data[idx_start:, 19])
plt.show()

# plot indexes
plt.plot(data[idx_start:, 20])
plt.plot(data[idx_start:, 21])
plt.legend(['usdx', 'eurx'], loc='best')
plt.show()


# """Chi-square."""
# from sklearn.feature_selection import chi2
# from sklearn.feature_selection import SelectKBest

# # x_chi = SelectKBest(chi2, k=10).fit_transform(np.abs(data_x), data_y)
# kbest = SelectKBest(chi2, k=20).fit(np.abs(data_x), data_out)
# kbest.scores_
# kbest.pvalues_
# plt.plot(kbest.scores_)
# plt.show()
# plt.plot(kbest.pvalues_)
# plt.show()


"""Recursive feature elimination."""
from sklearn.feature_selection import RFE
from sklearn.linear_model import SGDClassifier, RidgeClassifier

# select 10 the most informative features
# x_rfe = RFE(LinearRegression(), 10).fit_transform(data_x, data_y)
selectorR = RFE(RidgeClassifier(alpha=0.01, normalize=True), 20).fit(data_x, data_out)
selectorR.support_
selectorR.ranking_
# plt.plot(selectorR.support_)
# plt.plot(selectorR.ranking_)
# plt.show()
selectorS = RFE(SGDClassifier(), 20).fit(data_x, data_out)
selectorS.support_
selectorS.ranking_
# plt.plot(selectorS.support_)
# plt.plot(selectorS.ranking_)
# plt.show()


"""Ridge regression (L2)."""
from sklearn.linear_model import Ridge, RidgeClassifier

clr = Ridge(alpha=0.01, normalize=True)
clr.fit(data_x, data_out)
clr.coef_
# plt.plot(clr.coef_)
# plt.show()
clrcl = RidgeClassifier(alpha=0.01, normalize=True)
clrcl.fit(data_x, data_out)
clrcl.coef_
# plt.plot(clrcl.coef_[0])
# plt.plot(clrcl.coef_[1])
# plt.plot(clrcl.coef_[2])
# plt.show()


# """Lasso regression (L1)."""
# from sklearn.linear_model import Lasso

# cll = Lasso(alpha=0.01, normalize=True)
# cll.fit(data_x, data_out)
# cll.coef_
# plt.plot(cll.coef_)
# plt.show()


"""Table"""
col_names = ['metods', 'Year', 'Month', 'Day', 'DoW', 'DoY', 'h', 'm', 'Open', 'High', 'Low', 'Close',
                'Delta ', 'Delta ', 'Delta ', 'Delta ', 'Delta ', 'Delta ',
                'Derivative Open', 'Derivative High', 'Derivative Low', 'Derivative Close',
                'Logdiff Open', 'Logdiff High', 'Logdiff Low', 'Logdiff Close',
                'Sigmoid1', 'Sigmoid2', 'Sigmoid3', 'Sigmoid4',
                'Lowess 1/100', 'Lowess 1/250', 'Lowess 1/250 it=0', 'Close - EMA 13', 'Close - Lowess',
                'EMA 13', 'EMA 26', 'EMA 60', 'EMA 130', 'Delta EMA 13-26', 'Delta EMA 60-130',
                'derivative_ema1', 'derivative_ema2', 'derivative_ema3', 'derivative_ema4',
                'Logdiff EMA 13', 'Sigmoid EMA 13',
                'MACD Line', 'MACD Hist', 'ATR', 'CCI', 'RSI', 'USDX', 'EURX'
            ]
row_names = ['RFE Ridge', 'RFE SGD', 'Ridge Regr', 'Ridge Class']

import math

table = []
for row in range(5):
    for col in range(54):
        if row == 0:
            table.append(col_names[col])
        if row == 1:
            if col == 0:
                table.append(row_names[0])
            else:
                table.append(str(selectorR.support_[col-1]))
        if row == 2:
            if col == 0:
                table.append(row_names[1])
            else:
                table.append(str(selectorS.support_[col-1]))
        if row == 3:
            if col == 0:
                table.append(row_names[2])
            else:
                if abs(clr.coef_[col-1]) > 0.1:
                    table.append('True')
                else:
                    table.append('False')
        if row == 4:
            if col == 0:
                table.append(row_names[3])
            else:
                if abs(clrcl.coef_[0, col-1]) > 0.1:
                    table.append('True')
                else:
                    table.append('False')

path = 'E:/Projects/market-analysis-system/Market-Analysis (Keras)/researches/'
f_table = path + 'selected_features.csv'
np.savetxt(f_table, np.array(table).reshape(5, 54), delimiter=';', fmt='%s')

