## Catalog with data.
* /exported - Directory of original data exported from Alpari servers. [Link](https://goo.gl/q4S5Qu "GoogleDrive") to download the entire data in one archive.
* /transformed - The directory of the original data exported from Alpari servers, with the format `[datetime; open; high; low; close; volume]`. The following format of csv files is used by default in ML-Assistant and ML-DataSaver programs to save current quotes from the MetaTrader terminal. [Link](https://goo.gl/vCJNj6 "GoogleDrive") to download the entire data in one archive.
* /fractal dataset - Directory for storing data of one-symbol timeseries, united according to the principle - two timeframes, synchronized by lines.
* transform.py - A script that converts data exported from servers of brokers using MetaTrader to the format `[datetime; open; high; low; close; volume]`, which is used in ML-Assistant and ML-DataSaver programs.
* fractal_timeseries.py - A script that creates a dataset obtained by merging two timeframes of one symbol. **Note**: The algorithm requires refinement and optimization; Not suitable for working with large amounts of data.

## Каталог с данными. 
* /exported - Директория оригинальных данных экспортированных с серверов Alpari. [Ссылка](https://goo.gl/q4S5Qu "GoogleDrive") на скачивание всего датасета одним архивом.
* /transformed - Директория оригинальных данных экспортированных с серверов Alpari, с форматом `[datetime;open;high;low;close;volume]`. Следующий формат csv файлов используется по умолчанию в программах ML-Assistant и ML-DataSaver для сохранения текущих котировок из терминала MetaTrader. [Ссылка](https://goo.gl/vCJNj6 "GoogleDrive") на скачивание всего датасета одним архивом.
* /fractal dataset - Директория для сохранения данных таймсерий одного символа, объединенных по принципу - два таймфрейма, синронизированные по строкам.
* transform.py - Скрипт, который конвертирует данные экспортированные с серверов брокеров использующих MetaTrader, в формат `[datetime;open;high;low;close;volume]`, который используется в программах ML-Assistant и ML-DataSaver.
* fractal_timeseries.py - Скрипт, который создает датасет полученный путем слияния двух таймфреймов одного символа. **Примечание**: Алгоритм требует доработки и оптимизации; Не подходит для работы с большим количеством данных.
