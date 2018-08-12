import time
import numpy as np
import matplotlib.pyplot as plt

# import mas_tools.models.autoencoders as vae
from models import deep_conv2d_vae

from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau

from sklearn.model_selection import train_test_split
from mas_tools.ml import plot_history

wpath = 'E:/Projects/market-analysis-system/mas_vae/'
lpath = 'E:/Projects/market-analysis-system/data/windowed/'

symbols = ['GBPCHF', 'GBPJPY', 'GBPUSD', 'NZDJPY']
window = 20
prefix = 'norm_w20'
tf = '240.csv'
model_name = 'conv_ae_20_'

data = np.ones((window,), dtype=np.float)
data = np.reshape(data, (1, window))

start_t = time.clock()
for symbol in symbols:
    new_data = np.genfromtxt(lpath+prefix+symbol+tf, delimiter=';')
    new_data = np.reshape(new_data, (len(new_data), window, 4))
    new_data = np.reshape(new_data[:, :, 3], (len(new_data), window))
    data = np.vstack((data, new_data))
data = np.reshape(data[1:, :], (len(data)-1, 1, window))
x_train, x_test = train_test_split(data, shuffle=True, test_size=0.1)
data = None # Clear memory

print('New data shape: {} \nRead+Calc time: {}'.format(x_train.shape, time.clock()-start_t))


# Train AE
encoder, decoder, autoencoder, loss = deep_conv2d_vae((1, window))

autoencoder.compile(optimizer='adam', loss='mape', metrics=['acc'])

# autoencoder.load_weights(wpath+model_name+'_ended.hdf5', by_name=True)

reduce_lr = ReduceLROnPlateau(factor=0.1, patience=3, min_lr=0.00001, verbose=1)
checkpointer = ModelCheckpoint(wpath+model_name+'{epoch:02d}-{val_loss:.2f}.hdf5', verbose=0, save_best_only=True)

history = autoencoder.fit(x_train, x_train,
                            epochs=10,
                            batch_size=1024,
                            shuffle=True,
                            callbacks=[checkpointer, reduce_lr],
                            validation_data=(x_test, x_test))

autoencoder.save_weights(wpath+model_name+'_ended.hdf5')

# View
plot_history(history, acc='acc')


for n in [3000, 1500, 9000]:
    code = encoder.predict(x_test[n].reshape((1, 1, window)), batch_size=1)
    y_test = decoder.predict(code[2], batch_size=1)

    # plt.plot(x_test[n, 0, :])
    # plt.plot(y_test[0, 0, :])
    print(code[2])
    plt.plot(x_test[n, 0, :])
    plt.plot(y_test[0, 0, :])
    plt.ylabel('price')
    plt.xlabel('bar')
    plt.legend(['open_true', 'open_decoded', 'close_true', 'close_decoded'])
    plt.show()

