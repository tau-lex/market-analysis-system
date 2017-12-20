import matplotlib.pyplot as plt
# import numpy as np
from matplotlib.backends.backend_pdf import PdfPages


path = 'E:/Projects/market-analysis-system/Market-Analysis (Keras)/mas_research/'
optimizers = ['RMSprop', 'SGD', 'Adagrad', 'Adadelta', 'Adam', 'Adamax', 'Nadam']
losses = ['mse', 'mae', 'mape', 'msle', 'squared_hinge', 'hinge', \
          'kullback_leibler_divergence', 'poisson', 'cosine_proximity', 'binary_crossentropy']

#pp = PdfPages('_research_table.pdf')

fig, axes = plt.subplots(len(losses), len(optimizers))

i = -1
for ax in axes:
    i += 1
    img = path + optimizers[opt] + '-' + losses[loss] + '_EURUSD.pro1440_prediction.png'
    fig.figimage(plt.imread(img))

plt.axis('off')

#for opt in range(len(optimizers)-1):
#    for loss in range(len(losses)-1):
#        axes[loss, opt] = (opt * 432, loss * 288, (opt + 1) * 432, (loss + 1) * 288)
#        fig.sca(axes[loss, opt])
#        img = path + optimizers[opt] + '-' + losses[loss] + '_EURUSD.pro1440_prediction.png'
#        fig.figimage(plt.imread(img))

plt.figure(figsize=(432 * 7 / 72, 288 * 10 / 72))
#plt.plot()
#pp.savefig(fig)
#pp.close()
