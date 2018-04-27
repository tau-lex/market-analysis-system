
import math
import matplotlib.pyplot as plt
import numpy as np

from market_analysis_system.include import get_parameters, plot_history
from market_analysis_system.data import create_timeseries_matrix
from market_analysis_system.data import get_delta, get_diff, get_log_diff
from market_analysis_system.data import get_sigmoid_to_zero, get_sigmoid_ration
from market_analysis_system.models import save_model, load_model
from market_analysis_system.classes import signal_to_class, class_to_signal


#=============================================================================#
#       P R E P A R E   V A R I A B L E S                                     #
#=============================================================================#
limit = 6000
ts_lookback = 12

nclasses = 3
normalize_class = True

np.random.seed(13)


path = 'C:/Users/Alexey/AppData/Roaming/MetaQuotes/Terminal/287469DEA9630EA94D0715D755974F1B/MQL4/Files/ML-Assistant/'
workfile = 'EURUSD15'
file_x = path + workfile + '_x.csv'
file_y = path + workfile + '_y.csv'
prefix = 'tmp/data_x_'
model = None
data_x = np.array([])
data_y = np.array([])
train_x = np.array([])
train_y = np.array([])
test_x = np.array([])
test_y = np.array([])
history = None

# print('Backend:', backend())
print('\nWork file:', workfile)


#=============================================================================#
#       L O A D   D A T A                                                     #
#=============================================================================#
print('Loading Data...')

train_data = np.genfromtxt(file_x, delimiter=';')
target_data = np.genfromtxt(file_y, delimiter=';')

data, data_y = train_data[-limit:,], target_data[-limit:]
# for market(0, 3), ema(4, 7), macd(8, 9)
sigmoid = get_sigmoid_ration
sigm0 = sigmoid(data[:, 0])
sigm1 = sigmoid(data[:, 1])
sigm2 = sigmoid(data[:, 2])
sigm3 = sigmoid(data[:, 3])
delta_oc = get_delta(data, 0, 3)
diff1 = get_diff(data[:, 1])
diff2 = get_diff(data[:, 2])
diff3 = get_diff(data[:, 3])
logdiff1 = get_log_diff(data[:, 1])
logdiff2 = get_log_diff(data[:, 2])
logdiff3 = get_log_diff(data[:, 3])
detrend1 = get_delta(data, 3, 4) # close - ema13
detrend2 = get_delta(data, 3, 5) # close - ema26
diff_ema1 = get_diff(data[:, 4])
diff_ema2 = get_diff(data[:, 5])
delta_ema1 = get_delta(data, 4, 5)
delta_ema2 = get_delta(data, 6, 7)

data_y = signal_to_class(data_y, n=nclasses, normalize=normalize_class)
data_x, data_y = create_timeseries_matrix(train_data, data_y, ts_lookback)

# batch_input_shape=(batch_size, timesteps, units)
# data_x = np.reshape(data_x, (data_x.shape[0], ts_lookback, train_data.shape[1]))

# For training validation
train_x, test_x, train_y, test_y = train_test_split(data_x, data_y, test_size=train_test)

print('Input data shape :', data_x.shape)
# print('Input data shape :', data_x.shape[0], data_x.shape[1], data_x.shape[2])
print('Train/Test :', len(train_y), '/', len(test_y))


plt.plot(predicted)
plt.title('Predict')
plt.ylabel('class')
plt.xlabel('bar')
plt.legend(['buy', 'hold', 'sell'])
plt.show()
