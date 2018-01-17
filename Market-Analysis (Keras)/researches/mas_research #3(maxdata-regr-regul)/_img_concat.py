from PIL import Image


def imagematrix(file):
    images = []
    for opt in range(len(optimizers)):
        line = []
        for loss in range(len(losses)):
            line.append(Image.open(optimizers[opt] + '-' +
                                   losses[loss] + file))
        images.append(line)
    return images


def concat(images):
    width, height = images[0][0].size  # size of element
    total_width = width * len(images[0])
    max_height = height * len(images)
    result = Image.new('RGBA', (total_width, max_height))  # common canvas

    y_offset = 0
    for line in images:
        x_offset = 0
        for element in line:
            result.paste(element, (x_offset, y_offset))
            x_offset += element.size[0]
        y_offset += line[0].size[1]
    return result


postfix1 = '_EURUSD1440_accuracy.png'
postfix2 = '_EURUSD1440_loss.png'
postfix3 = '_EURUSD1440_prediction.png'
postfix4 = '_EURUSD1440_input-weights.png'
optimizers = ['RMSprop', 'Adagrad', 'Adadelta', 'Adam', 'Adamax', 'Nadam'] #del 'SGD'
losses = ['mse', 'mae', 'mape', 'msle', 'squared_hinge', 'hinge', \
          'kullback_leibler_divergence', 'binary_crossentropy'] #del 'cosine_proximity', 'poison'

concat(imagematrix(postfix1)).save('_research_table' + postfix1)
concat(imagematrix(postfix2)).save('_research_table' + postfix2)
concat(imagematrix(postfix3)).save('_research_table' + postfix3)
concat(imagematrix(postfix4)).save('_research_table' + postfix4)

