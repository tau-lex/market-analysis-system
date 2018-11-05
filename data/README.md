## Data En
Directory for storing and transforming data necessary for training models.
* /exported - Directory of original data exported from Alpari servers. [Link](https://goo.gl/q4S5Qu "GoogleDrive") to download the entire data in one archive.
* /transformed - Directory of the original data exported from Alpari servers, with the format `[datetime; open; high; low; close; volume]`. The following format of csv files is used by default in [ML-Assistant](https://github.com/terentjew-alexey/mql_projects/blob/master/MASi_ML-Assistant.mq4 "Github") and [ML-DataSaver](https://github.com/terentjew-alexey/mql_projects/blob/master/MASi_ML-DataSaver.mq4 "Github") programs to save current quotes from the MetaTrader terminal. [Link](https://goo.gl/vCJNj6 "GoogleDrive") to download the entire data in one archive.
* /normalized - Directory for data normalized to 1.0.
* /windowed - Directory of data in the form of a sequence of observation windows.
* /pictured - Directory with windows of time series converted into images.

## Data Ru
Каталог для хранения и трансформации данных необходимых для обучения моделей.
* /exported - Директория оригинальных данных экспортированных с серверов Alpari. [Ссылка](https://goo.gl/q4S5Qu "GoogleDrive") на скачивание всего датасета одним архивом.
* /transformed - Директория оригинальных данных экспортированных с серверов Alpari, с форматом `[datetime;open;high;low;close;volume]`. Следующий формат csv файлов используется по умолчанию в программах [ML-Assistant](https://github.com/terentjew-alexey/mql_projects/blob/master/MASi_ML-Assistant.mq4 "Github") и [ML-DataSaver](https://github.com/terentjew-alexey/mql_projects/blob/master/MASi_ML-DataSaver.mq4 "Github") для сохранения текущих котировок из терминала MetaTrader. [Ссылка](https://goo.gl/vCJNj6 "GoogleDrive") на скачивание всего датасета одним архивом.
* /normalized - Директория для данных нормированных к 1.0.
* /windowed - Директория данных в виде последовательности окон наблюдения.
* /pictured - Директория с окнами временных рядов преобразованных в изображения.
