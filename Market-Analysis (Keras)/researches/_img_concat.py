from PIL import Image


def imagematrix(_rows, _columns, _pref, _post):
    images = []
    for row in _rows:
        line = []
        for col in _columns:
            line.append(Image.open(_pref + row + col + _post))
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

path = 'E:/Projects/market-analysis-system/Market-Analysis (Keras)/researches/'
prefix, postfix = path + 'ridge-l2', '.png'
columns = ['', '-norm']
rows = ['-1.0', '-0.1', '-0.01']
concat(imagematrix(rows, columns, prefix, postfix)).save(prefix + '_table' + postfix)

prefix, postfix = path + 'ridge-cl-l2', '.png'
concat(imagematrix(rows, columns, prefix, postfix)).save(prefix + '_table' + postfix)

prefix, postfix = path + 'rfe-', '.png'
columns = ['ridge-cl-', 'sgd-cl-']
rows = ['10', '20']
concat(imagematrix(columns, rows, prefix, postfix)).save(prefix + '_table' + postfix)

