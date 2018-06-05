"""
https://stackoverflow.com/questions/36252434/predicting-on-new-data-using-locally-weighted-regression-loess-lowess
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from statsmodels.nonparametric.smoothers_lowess import lowess


def test0():
    x = np.random.uniform(low = -2*np.pi, high = 2*np.pi, size=250)
    y = np.sin(x) + np.random.normal(size=len(x))

    z = lowess(y, x)
    w = lowess(y, x, frac=1./3)
    v = lowess(y, x, frac= 1./3, it=0)

    # plt.plot(x, y, color='red')
    plt.plot(z[:,0], z[:,1], color='green')
    plt.plot(w[:,0], w[:,1], color='blue')
    plt.plot(v[:,0], v[:,1], color='cyan')
    plt.show()


def test2():
    # introduce some floats in our x-values
    # ввести некоторые float в значения x
    x = list(range(3, 33)) + [3.2, 6.2]
    y = [1,2,1,2,1,1,3,4,5,4,5,6,5,6,7,8,9,10,11,11,12,11,11,10,12,11,11,10,9,8,2,13]

    # lowess will return our "smoothed" data with a y value for at every x-value
    # lowess вернет наши «сглаженные» данные с помощью значения y для каждого значения x
    lwss = lowess(y, x, frac=.3)

    # unpack the lowess smoothed points to their values
    # распакуйте сглаженные точки с их значениями
    lowess_x = list(zip(*lwss))[0]
    lowess_y = list(zip(*lwss))[1]

    # run scipy's interpolation. There is also extrapolation I believe
    # запустить интерполяцию scipy. Есть также экстраполяция, которую я считаю
    f = interp1d(lowess_x, lowess_y, bounds_error=False)

    xnew = [i/10. for i in range(400)]

    # this this generate y values for our xvalues by our interpolator
    # it will MISS values outsite of the x window (less than 3, greater than 33)
    # There might be a better approach, but you can run a for loop
    #and if the value is out of the range, use f(min(lowess_x)) or f(max(lowess_x))
    # this это порождает значения y для наших значений x нашим интерполятором
    # он будет MISS значения outsite из окна x (менее 3, больше 33)
    # Может быть, есть лучший подход, но вы можете запустить цикл for
    #, и если значение вне диапазона, используйте f (min (lowess_x)) или f (max (lowess_x))
    ynew = f(xnew)

    plt.plot(x, y, 'o')
    plt.plot(lowess_x, lowess_y, '*')
    plt.plot(xnew, ynew, '-')
    plt.show()


def test3():
    data = pd.read_table("data.dat", sep=",", names=["time", "pressure"])
    sub_data = data

    result = lowess(sub_data.pressure, sub_data.time.values)
    x_smooth = result[:,0]
    y_smooth = result[:,1]

    tot_result = lowess(data.pressure, data.time.values, frac=0.1)
    x_tot_smooth = tot_result[:,0]
    y_tot_smooth = tot_result[:,1]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(data.time.values, data.pressure, label="raw")
    ax.plot(x_tot_smooth, y_tot_smooth, label="lowess 1%", linewidth=3, color="g")
    ax.plot(x_smooth, y_smooth, label="lowess", linewidth=3, color="r")
    plt.legend()
    