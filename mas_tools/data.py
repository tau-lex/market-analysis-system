# -*- coding: utf-8 -*-
from math import exp

import numpy as np
from numpy.random import shuffle
from PIL import Image, ImageDraw


def create_timeseries_matrix(data_x, data_y=[], look_back=3):
    """Converts a dataset into a time series matrix.
    
    Arguments
        data_x (array like): Features data.
        data_y (array like): Target data.
        look_back (int): size of minibatches.
        
    Returns
        data_x (array): Transformed features data.
        data_y (array): Transformed target data."""

    if look_back <= 1:
        return np.array(data_x), np.array(data_y)

    if look_back >= data_x.shape[0]:
        print('create_timeseries_matrix() error = look back size is large')
        return np.array(data_x), np.array(data_y)

    back = look_back - 1
    len_x = len(data_x)
    data_x = np.array(data_x)
    data_y = np.array(data_y)

    lshape = len(data_x.shape)
    if lshape > 1:
        result = np.array(data_x[:-back, :])
    else:
        result = np.array(data_x[:-back])

    for i in range(1, look_back):
        j = len_x - back + i
        if lshape > 1:
            result = np.hstack((result, data_x[i:j, :]))
        else:
            result = np.vstack((result, data_x[i:j]))

    if lshape > 1:
        new_shape = (data_x.shape[0] - look_back + 1, data_x.shape[1] * look_back)
    else:
        new_shape = (data_x.shape[0] - look_back + 1, look_back)
        result = result.T
    result = np.reshape(result, new_shape)

    return result, data_y[back:]


def dataset_to_traintest(data, train_ratio=0.6, limit=0):
    """Returns a data set divided into two matrices.
    train = train_ratio * data.
    limit > 0 - limits the size of the dataset.
    ! Depricated."""

    data = np.array(data)

    start, size = 0, len(data)
    if limit > 0:
        if size > limit:
            start, size = size - limit, limit
    elif limit < 0:
        if size > abs(limit):
            start, size = 0, abs(limit)

    if train_ratio <= 0.0:
        return None, data[start:size, :]
    elif train_ratio >= 1.0:
        return data[start:size, :], None

    train_size = int(size * train_ratio)
    # test_size = len(data) - train_size

    if len(data.shape) == 1:
        return data[start:(start + train_size),], data[(start + train_size):len(data),]
    return data[start:(start + train_size), :], data[(start + train_size):len(data), :]


def shuffle_xy(data_a = [], data_b = []):
    """Shuffle data sets."""

    data_a = np.array(data_a)
    data_b = np.array(data_b)
    try:
        width_a = data_a.shape[1]
        temp = np.hstack((data_a, data_b))
        shuffle(temp)
    except:
        print('Exception: non equal shapes. A:', data_a.shape, 'B:', data_b.shape)
        return data_a, data_b
        
    return np.hsplit(temp, np.array([width_a]))


def timeseries_to_img(data):
    """Creates an image of a time series window of the 'ohlc' type.
    
    Arguments
        data (array like): Input array size (window_size, 4).
        
    Returns
        img (Image object): PIL module image object."""

    width = len(data) * 4
    height = width

    mn = min(min(data[:, 0]), min(data[:, 1]), min(data[:, 2]), min(data[:, 3]))
    mx = max(max(data[:, 0]), max(data[:, 1]), max(data[:, 2]), max(data[:, 3]))

    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    def norm_height(value):
        val = (value - mn) / (mx - mn) * height # scale
        return height - val                     # invert

    pix = img.load()
    for idx in range(len(data)):
        bar = data[idx]
        x = (idx + 1) * 4 - 2
        o = norm_height(bar[0])
        h = norm_height(bar[1])
        l = norm_height(bar[2])
        c = norm_height(bar[3])
        clr_bar = 'red' if o < c else 'green'
        clr_line = (255, 0, 127) if o < c else (0, 255, 127)
        draw.rectangle((x-1, o, x+1, c), fill=clr_bar)
        draw.line((x, h, x, l), fill=clr_line, width=1)

    del draw

    return img


def get_delta(data, index1=0, index2=1):
    """Returns the difference between [,index1] and [,index2] in 2-D array."""

    return data[:, index1] - data[:, index2]


def get_deltas_from_ohlc(data, index1=0):
    """Calculates the delta prices (open, high, low, close) between index1 and index2.
    Returns the numpy array with the shape (:, 6): [O-C, H-L, H-O, H-C, O-L, C-L]"""

    return np.column_stack((get_delta(data, index1, index1 + 3),    # Open - Close
                                get_delta(data, index1 + 1, index1 + 2),# High - Low
                                get_delta(data, index1 + 1, index1),    # High - Open
                                get_delta(data, index1 + 1, index1 + 3),# High - Close
                                get_delta(data, index1, index1 + 2),    # Open - Low
                                get_delta(data, index1 + 3, index1 + 2) # Close - Low
                            ))


def get_diff(data, rate=1):
    """Computes a derivative and returns an array equal to
    the length of the original array."""

    result = np.array([])
    for idx in range(rate):
        result = np.append(result, 0.0)

    if rate == 1:
        return np.append(result, np.diff(data))

    for idx in range(rate, len(data)):
        result = np.append(result, data[idx] - data[idx-rate])

    return result


def get_log_diff(data, rate=1):
    """Computes the log-differential and returns an array equal to
    the length of the original array."""

    result = np.array([])
    for idx in range(rate):
        result = np.append(result, 0.0)

    for idx in range(rate, len(data)):
        ld = np.log(data[idx] / data[idx-rate])
        result = np.append(result, ld)

    return result


def get_sigmoid(data):
    """Sigmoid function."""

    result = 1 / (1 + np.exp(-data))
    # return exp(-np.logaddexp(0, -data))
    # return 0.5 * (1 + data / (1 + abs(data)))

    return result


def get_sigmoid_to_zero(data):
    """Sigmoid function."""

    result = 1 / (1 + np.exp(-data)) - 0.5

    return result


def get_sigmoid_stable(data):
    """Numerically-stable sigmoid function."""

    result = np.array([])
    z = 0.0

    for item in data:
        if item >= 0.0:
            z = 1.0 / (1 + exp(-data))
        else:
            z = 1.0 / (1 + exp(data))
        result = np.append(result, z)

    return result


def get_sigmoid_ration(data, alpha=2.0):
    """Rationaly sigmoid."""

    result = data / (np.abs(data) + alpha)

    return result
