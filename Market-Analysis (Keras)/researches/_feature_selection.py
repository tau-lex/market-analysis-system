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
sys.path.append('../')
from mas.classes import signal_to_class2, class2_to_signal

"""Load data."""
path = 'C:/Users/Alexey/AppData/Roaming/MetaQuotes/Terminal/287469DEA9630EA94D0715D755974F1B/MQL4/Files/ML-Assistant/'
symbol = 'EURUSD1440'
file_x = path + symbol + '_x.csv'
file_y = path + symbol + '_y.csv'

data_x = np.genfromtxt(file_x, delimiter=';')
data_y = np.genfromtxt(file_y, delimiter=';')


"""Transform data."""
# GOTO

"""Chi-square."""
from sklearn.feature_selection import chi2
from sklearn.feature_selection import SelectKBest

# x_chi = SelectKBest(chi2, k=10).fit_transform(np.abs(data_x), data_y)
kbest = SelectKBest(chi2, k=10).fit(np.abs(data_x), data_y)
kbest.scores_
kbest.pvalues_


"""Recursive feature elimination."""
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression

lr = LinearRegression()
# select 10 the most informative features
# x_rfe = RFE(lr, 10).fit_transform(data_x, data_y)
selector = RFE(lr, 10).fit(data_x, data_y)
selector.support_
selector.ranking_


"""Ridge regression (L2)."""
from sklearn.linear_model import Ridge

clr = Ridge(alpha=0.1)
clr.fit(data_x, data_y)
clr.coef_


"""Lasso regression (L1)."""
from sklearn.linear_model import Lasso

cll = Lasso(alpha=0.01)
cll.fit(data_x, data_y)
cll.coef_

