import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import matthews_corrcoef

from keras.utils import plot_model


def plot_history(history, acc='accuracy'):
    """Plot functions graph."""

    # summarize history for accuracy
    plt.plot(history.history[acc])
    plt.plot(history.history['val_'+acc])
    plt.title('Model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    # plt.axhline(y=0.5, color='grey', linestyle='--')
    plt.show()

    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    # plt.axhline(y=0.5, color='grey', linestyle='--')
    plt.show()


def classification_scores(true_y, test_y, n=3):
    """"""

    if n <= 1:
        raise ValueError("classification scores")
    
    labels = range(n)
    if n == 2:
        names = ['pass', 'signal']
    elif n == 3:
        names = ['hold', 'buy', 'sell']
    
    # TODO check data

    result = '-' * 20
    result += '\n\nMATTHEWS CORRELATION:\n'
    result += matthews_corrcoef(true_y, test_y)

    result += '\n\nCONFUSION MATRIX:\n'
    cm = confusion_matrix(true_y, test_y, labels=labels)
    result += cm / cm.astype(np.float).sum(axis=1)

    result += '\n\nCLASSIFICATION REPORT:\n'
    result += classification_report(true_y, test_y,
                                    labels=labels,
                                    target_names=names)
    result += '\n' + '-' * 20

    return result


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    
    Arguments
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    plt.figure()
    
    print(cm)
    
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(classes)
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def save_model_arch(model, name):
    """Save model architecture."""
    plot_model(model, to_file=name+'.png',
                show_shapes=True,
                show_layer_names=False)

    text = ''
    for item in model.layers:
        text = text + str(item.name) + '\n'
        text = text + str(item.input_shape) + '\n'
        text = text + str(item.output_shape) + '\n'
        # text = text + str(item.get_weights()) + '\n'
        text = text + '\n=====================================\n'

    f = open(name+'.txt', 'w')
    f.write(text)
    f.close()

