
import matplotlib.pyplot as plt
from keras.models import Model, model_from_json

def load_model(filename: str):
    json_string = ''
    try:
        file = open(filename, 'r')
    except IOError as exc:
        print('Error! Model file not find', exc)
    else:
        json_string = file.read()
        file.close()
    if len(json_string) > 0:
        model = model_from_json(json_string)
        return model


optimizers = ['RMSprop', 'SGD', 'Adagrad', 'Adadelta', 'Adam', 'Adamax', 'Nadam']
losses = ['mse', 'mae', 'mape', 'msle', 'squared_hinge', 'hinge', 'poisson', \
          'cosine_proximity', 'kullback_leibler_divergence', 'binary_crossentropy']

symbol = '_EURUSD1440'
model = Model([], [])

for opt in optimizers:
    for loss in losses:
        file_model = opt + '-' + loss + symbol + '.model'
        file_weights = opt + '-' + loss + symbol + '.hdf5'

        model = load_model(file_model)
        model.load_weights(file_weights)
        input_w = model.get_layer(index=2).get_weights()[0][0]

        plt.plot(input_w)
        plt.title('Trained first layer | ' + opt + ' ' + loss)
        plt.ylabel('weight')
        plt.xlabel('feature')
#        plt.show()
        plt.savefig(opt + '-' + loss + symbol + '_input-weights.png')
        plt.close()
