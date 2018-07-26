import numpy as np

from mas_tools.utils.data import create_timeseries_matrix
import mas_tools.layers.autoencoders as vae

from sklearn.model_selection import train_test_split
from mas_tools.utils.ml import plot_history


file_x = 'E:/Projects/market-analysis-system/data/transformed/EURUSD15.csv'


# Load Data
data_x = np.genfromtxt(file_x, delimiter=';')[:, 1:5]

data_x, _ = create_timeseries_matrix(data_x, look_back=20)
data_x = np.reshape(data_x, (len(data_x), 20, 4))

x_train, x_test = train_test_split(data_x, test_size=0.2)


# Train AE
encoder, decoder, autoencoder = vae.create_dense_ae((20, 4), 32)

autoencoder.compile(optimizer='adam', loss='mse', metrics=['acc'])

history = autoencoder.fit(x_train, x_train,
                            epochs=10,
                            batch_size=256,
                            shuffle=True,
                            validation_data=(x_test, x_test))


# View
plot_history(history, acc='acc')

n = 100

test_x = x_test[n]
test_code = encoder.predict(test_x)
test_y = decoder.predict(test_code)

delta = test_x - test_y

import matplotlib.pyplot as plt

plt.plot(delta[:, 0])
plt.show()
# imgs = x_test[:n]
# encoded_imgs = encoder.predict(imgs, batch_size=n)
# encoded_imgs[0]

# decoded_imgs = decoder.predict(encoded_imgs, batch_size=n)

# plot_digits(imgs, decoded_imgs)
