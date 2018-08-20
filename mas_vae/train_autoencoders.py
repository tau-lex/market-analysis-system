import time
import numpy as np
import matplotlib.pyplot as plt

# import mas_tools.models.autoencoders as vae
from mas_vae.models import deep_conv2d_vae, plot_results

from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau

from sklearn.model_selection import train_test_split
from mas_tools.ml import plot_history

wpath = 'E:/Projects/market-analysis-system/mas_vae/'
lpath = 'E:/Projects/market-analysis-system/data/pictured/'

symbols = ['GBPCHF', 'GBPJPY', 'GBPUSD', 'NZDJPY']
window = 20
# prefix = 'norm_w20'
tf = '240_w20.npz'
# tf = '1_w20.npz'
model_name = 'conv_vae_20_'
batch = 128
img_width = window * 4
img_size = window*4 * window*4 * 3


#====== load data ======
data = np.ones((img_size,), dtype=np.float)
data = np.reshape(data, (1, img_width, img_width, 3))

start_t = time.clock()
for symbol in symbols:
    npz_file = np.load(lpath + symbol + tf)
    new_data = npz_file.f.arr_0
    # new_data = np.genfromtxt(lpath+prefix+symbol+tf, delimiter=';')
    new_data = np.reshape(new_data, (len(new_data), img_width, img_width, 3))
    data = np.vstack((data, new_data))
data = data[1:]
x_train, x_test = train_test_split(data, shuffle=True, test_size=0.1)
data = None # Clear memory

print('New data shape: {} \nRead+Calc time: {}'.format(x_train.shape, time.clock()-start_t))


#====== Train AE ======
encoder, decoder, autoencoder, loss = deep_conv2d_vae((img_width, img_width, 3))

autoencoder.compile(optimizer='adam', loss='mae', metrics=['acc'])

# autoencoder.load_weights(wpath+model_name+'_ended.hdf5', by_name=True)

reduce_lr = ReduceLROnPlateau(factor=0.1, patience=3, min_lr=0.00001, verbose=1)
checkpointer = ModelCheckpoint(wpath+model_name+'{epoch:02d}-{val_loss:.4f}.hdf5',
                                verbose=0, save_best_only=True)

history = autoencoder.fit(x_train, x_train,
                            epochs=2,
                            batch_size=batch,
                            shuffle=True,
                            callbacks=[checkpointer, reduce_lr],
                            validation_data=(x_test, x_test))

autoencoder.save_weights(wpath+model_name+'_ended.hdf5')


#====== View ======
plot_history(history, acc='acc')

plot_results((encoder, decoder),
             (x_test, x_test),
             batch_size=batch,
             w=window)
             
# for n in [3000, 1500, 9000]:
#     code = encoder.predict(x_test[n].reshape((1, img_width, img_width, 3)), batch_size=1)
#     y_test = decoder.predict(code[2], batch_size=1)

#     # plt.plot(x_test[n, 0, :])
#     # plt.plot(y_test[0, 0, :])
#     print(code[2])
#     plt.plot(x_test[n, 0, :])
#     plt.plot(y_test[0, 0, :])
#     plt.ylabel('price')
#     plt.xlabel('bar')
#     plt.legend(['open_true', 'open_decoded', 'close_true', 'close_decoded'])
#     plt.show()

