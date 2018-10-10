## Catalog with data.
Directory for storing and transforming data necessary for training models.
* /exported - Directory of original data exported from Alpari servers. [Link](https://goo.gl/q4S5Qu "GoogleDrive") to download the entire data in one archive.
* /fractal dataset - Directory for storing data of one-symbol timeseries, united according to the principle - two timeframes, synchronized by lines.
* /normalized - Directory for data normalized to 1.0.
* /pictured - Directory with windows of time series converted into images.
* /transformed - Directory of the original data exported from Alpari servers, with the format `[datetime; open; high; low; close; volume]`. The following format of csv files is used by default in [ML-Assistant](https://github.com/terentjew-alexey/mql_projects/blob/master/MASi_ML-Assistant.mq4 "Github") and [ML-DataSaver](https://github.com/terentjew-alexey/mql_projects/blob/master/MASi_ML-DataSaver.mq4 "Github") programs to save current quotes from the MetaTrader terminal. [Link](https://goo.gl/vCJNj6 "GoogleDrive") to download the entire data in one archive.
* /windowed - Directory of data in the form of a sequence of observation windows.

## Каталог с данными.
Директория для хранения и трансформации данных необходимых для обучения моделей.
* /exported - Директория оригинальных данных экспортированных с серверов Alpari. [Ссылка](https://goo.gl/q4S5Qu "GoogleDrive") на скачивание всего датасета одним архивом.
* /fractal dataset - Директория для сохранения данных таймсерий одного символа, объединенных по принципу - два таймфрейма, синронизированные по строкам.
* /normalized - Директория для данных нормированных к 1.0.
* /pictured - Директория с окнами временных рядов преобразованных в изображения.
* /transformed - Директория оригинальных данных экспортированных с серверов Alpari, с форматом `[datetime;open;high;low;close;volume]`. Следующий формат csv файлов используется по умолчанию в программах [ML-Assistant](https://github.com/terentjew-alexey/mql_projects/blob/master/MASi_ML-Assistant.mq4 "Github") и [ML-DataSaver](https://github.com/terentjew-alexey/mql_projects/blob/master/MASi_ML-DataSaver.mq4 "Github") для сохранения текущих котировок из терминала MetaTrader. [Ссылка](https://goo.gl/vCJNj6 "GoogleDrive") на скачивание всего датасета одним архивом.
* /windowed - Директория данных в виде последовательности окон наблюдения.
