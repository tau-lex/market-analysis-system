import time
import numpy as np
import matplotlib.pyplot as plt

from mas_tools.data import create_timeseries_matrix
import mas_tools.layers.autoencoders as vae
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau

from sklearn.model_selection import train_test_split
from mas_tools.ml import plot_history

wpath = 'E:/Projects/market-analysis-system/mas_vae/'
path = 'E:/Projects/market-analysis-system/data/transformed/'
files = ['EURUSD15.csv', 'AUDJPY15.csv', 'AUDUSD15.csv', 'CHFJPY15.csv',
        'EURAUD15.csv', 'EURCAD15.csv', 'EURCHF15.csv', 'EURGBP15.csv',
        'EURJPY15.csv', 'EURRUB15.csv']
# files = []

# Load Data
# file_x = path + files[0]
# data_x = np.genfromtxt(file_x, delimiter=';')[:, 1:5]
# data_x, _ = create_timeseries_matrix(data_x, look_back=20)
# data_x = np.reshape(data_x, (len(data_x), 20, 4))

data_x = np.ones((80,), dtype=np.float)
data_x = np.reshape(data_x, (1, 20, 4))

start_t = time.clock()
for fn in files:
    new_data = np.genfromtxt(path+fn, delimiter=';')[:, 1:5]
    new_data, _ = create_timeseries_matrix(new_data, look_back=20)
    new_data = np.reshape(new_data, (len(new_data), 20, 4))
    data_x = np.vstack((data_x, new_data))

print('New data shape: {} \nRead+Calc time: {}'.format(data_x.shape, time.clock()-start_t))

x_train, x_test = train_test_split(data_x, test_size=0.1)
data_x = None # Clear memory


# Train AE
encoder, decoder, autoencoder = vae.create_deep_ae((20, 4), 64)

autoencoder.compile(optimizer='nadam', loss='mse')

autoencoder.load_weights(wpath+'ae_deep_20-4_64.hdf5', by_name=True)

reduce_lr = ReduceLROnPlateau(factor=0.1, patience=3, min_lr=0.00001, verbose=1)
checkpointer = ModelCheckpoint(wpath+'ae_deep_{epoch:02d}-{val_loss:.2f}.hdf5', verbose=0, save_best_only=True)

history = autoencoder.fit(x_train, x_train,
                            epochs=10,
                            batch_size=512,
                            shuffle=True,
                            callbacks=[checkpointer, reduce_lr],
                            validation_data=(x_test, x_test))

autoencoder.save_weights(wpath+'ae_deep_20-4_64.hdf5')


# View
plot_history(history, acc='acc')

nb = [3000, 15000, 29000]

for n in nb:
    code = encoder.predict(x_test[n].reshape((1, 20, 4)), batch_size=1)
    y_test = decoder.predict(code, batch_size=1)

    plt.plot(x_test[n, :, 0])
    plt.plot(y_test[0, :, 0])
    plt.plot(x_test[n, :, 3])
    plt.plot(y_test[0, :, 3])
    plt.ylabel('price')
    plt.xlabel('bar')
    plt.legend(['open_true', 'open_decoded', 'close_true', 'close_decoded'])
    plt.show()

