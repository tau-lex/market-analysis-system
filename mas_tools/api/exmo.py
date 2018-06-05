## https://exmo.me/ru/api

## Public API

# trades        (POST или GET)
# Параметры:    pair - одна или несколько валютных пар разделенных запятой (пример BTC_USD,BTC_EUR)
# Пример:       https://api.exmo.com/v1/trades/?pair=BTC_USD
#
# {"BTC_USD": [{
#     "trade_id": 3,        # идентификатор сделки
#     "type": "sell",       # тип сделки
#     "price": "100",       # цена сделки
#     "quantity": "1",      # кол-во по сделке
#     "amount": "100",      # сумма сделки
#     "date": 1435488248    # дата и время сделки в формате Unix
# }]}

# order_book    (POST или GET)
# Параметры:    pair - одна или несколько валютных пар разделенных запятой (пример BTC_USD,BTC_EUR)
#               limit - кол-во отображаемых позиций (по умолчанию 100, максимум 1000)
# Пример:       https://api.exmo.com/v1/order_book/?pair=BTC_USD
#
# {"BTC_USD": {
#     "ask_quantity": "3",      # объем всех ордеров на продажу
#     "ask_amount": "500",      # сумма всех ордеров на продажу
#     "ask_top": "100",         # минимальная цена продажи
#     "bid_quantity": "1",      # объем всех ордеров на покупку
#     "bid_amount": "99",       # сумма всех ордеров на покупку
#     "bid_top": "99",          # максимальная цена покупки
#     "ask": [[100,1,100],[200,2,400]], # список ордеров на покупку, где каждая строка это цена, количество и сумма
#     "bid": [[99,1,99]]                # список ордеров на продажу, где каждая строка это цена, количество и сумма
# }}

# ticker    (POST или GET)
# Пример: 	https://api.exmo.com/v1/ticker/
#
# {"BTC_USD": {
#     "buy_price": "589.06",    # текущая максимальная цена покупки
#     "sell_price": "592",      # текущая минимальная цена продажи
#     "last_trade": "591.221",  # цена последней сделки
#     "high": "602.082",        # максимальная цена сделки за 24 часа
#     "low": "584.51011695",    # минимальная цена сделки за 24 часа
#     "avg": "591.14698808",    # средняя цена сделки за 24 часа
#     "vol": "167.59763535",    # объем всех сделок за 24 часа
#     "vol_curr": "99095.17162071", # сумма всех сделок за 24 часа
#     "updated": 1470250973         # дата и время обновления данных
# }}

# pair_settings (POST или GET)
# Пример:       https://api.exmo.com/v1/pair_settings/
#
# {"BTC_USD": {
#     "min_quantity": "0.001",  # минимальное кол-во по ордеру
#     "max_quantity": "100",    # максимальное кол-во по ордеру
#     "min_price": "1",         # минимальная цена по ордеру
#     "max_price": "10000",     # максимальная цена по ордеру
#     "max_amount": "30000",    # максимальная сумма по ордеру
#     "min_amount": "1"         # минимальная сумма по ордеру
# }}

# currency  (POST или GET)
# Пример:   https://api.exmo.com/v1/currency/
#
# ["USD","EUR","RUB","BTC","DOGE","LTC"]


## Authenticated API

# Для доступа к данному API требуется авторизация 
# и необходимо использовать POST метод.
# URL — необходимо использовать следующий 
# адрес https://api.exmo.com/v1/{api_name},
# где api_name - это наименование API метода
#
# Авторизация осуществляется с помощью отправки на сервер следующих заголовков:
#
# Key — Публичный ключ, его нужно взять настройках профиля пользователя
# (пример: K-7cc97c89aed2a2fd9ed7792d48d63f65800c447b)
#
# Sign — POST данные (param=val&param1=val1), подписанные секретным ключом 
# методом HMAC-SHA512, секретный ключ также нужно брать в настройках профиля 
# пользователя
#
# Дополнительно во всех запросах должен находиться обязательный POST-параметр
# nonce с инкрементным числовым значением (>0). Это значение 
# не должно повторяться или уменьшаться.

import sys
import time
import json
import http.client
import urllib
import hashlib
import hmac

class ExmoAPI:
    def __init__(self, API_KEY, API_SECRET, API_URL = 'api.exmo.com', API_VERSION = 'v1'):
        self.API_URL = API_URL
        self.API_VERSION = API_VERSION
        self.API_KEY = API_KEY
        self.API_SECRET = bytes(API_SECRET, encoding='utf-8')

    def sha512(self, data):
        H = hmac.new(key = self.API_SECRET, digestmod = hashlib.sha512)
        H.update(data.encode('utf-8'))
        return H.hexdigest()

    def api_query(self, api_method, params = {}):
        params['nonce'] = int(round(time.time() * 1000))
        params =  urllib.parse.urlencode(params)

        sign = self.sha512(params)
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Key": self.API_KEY,
            "Sign": sign
        }
        conn = http.client.HTTPSConnection(self.API_URL)
        conn.request("POST", "/" + self.API_VERSION + "/" + api_method, params, headers)
        response = conn.getresponse().read()

        conn.close()

        try:
            obj = json.loads(response.decode('utf-8'))
            if 'error' in obj and obj['error']:
                print(obj['error'])
                raise sys.exit()
            return obj
        except json.decoder.JSONDecodeError:
            print('Error while parsing response:', response)
            raise sys.exit()

# Example
ExmoAPI_instance = ExmoAPI('YOUR API KEY', 'YOUR API SECRET')
print(ExmoAPI_instance.api_query('user_info'))


# Наименование метода: 	user_info
# Тип запроса: 	POST
# Входящие параметры: 	Отсутствуют
# Пример использования: 	api_query("user_info", Array());
# Возращаемое значение: 	
# {
#   "uid": 10542,
#   "server_date": 1435518576,
#   "balances": {
#     "BTC": "970.994",
#     "USD": "949.47"
#   },
#   "reserved": {
#     "BTC": "3",
#     "USD": "0.5"
#   }
# }
# Описание полей:
# uid - идентификатор пользоватля
# server_date - дата и время сервера
# balances - доступный баланс пользователя
# reserved - баланс пользователя в ордерах


# Создание ордера
# Наименование метода: 	order_create
# Тип запроса: 	POST
# Входящие параметры: 	
# pair - валютная пара
# quantity - кол-во по ордеру
# price - цена по ордеру
# type - тип ордера, может принимать следующие значения:
#     buy - ордер на покупку
#     sell - ордер на продажу
#     market_buy - ордера на покупку по рынку
#     market_sell - ордер на продажу по рынку
#     market_buy_total - ордер на покупку по рынку на определенную сумму
#     market_sell_total - ордер на продажу по рынку на определенную сумму
# Возращаемое значение: 	
# {
#   "result": true,
#   "error": "",
#   "order_id": 123456
# }
# Описание полей: 	
# result - true в случае успешного создания и false в случае ошибки
# error - содержит текст ошибки
# order_id - идентификатор ордера


# Наименование метода: 	order_cancel
# Тип запроса: 	POST
# Входящие параметры: 	order_id - идентификатор ордера
# Пример использования:
# api_query("order_cancel", Array(
#     "order_id"=>104235
# ));
# Возращаемое значение:
# {
#   "result": true,
#   "error": ""
# }
# Описание полей: 	
# result - true в случае успешного создания задачи на отмену ордера 
# и false в случае ошибки
# error - содержит текст ошибки


# Получение списока открытых ордеров пользователя
# Наименование метода: 	user_open_orders
# Тип запроса: 	POST
# Входящие параметры: 	отсутствуют
# Пример использования: 	
# api_query("user_open_orders", Array());
# Возращаемое значение:
# {
#   "BTC_USD": [
#     {
#       "order_id": "14",
#       "created": "1435517311",
#       "type": "buy",
#       "pair": "BTC_USD",
#       "price": "100",
#       "quantity": "1",
#       "amount": "100"
#     }
#   ]
# }
# Описание полей: 	
# order_id - идентификатор ордера
# created - дата и время создания ордера
# type - тип ордера
# pair - валютная пара
# price - цена по ордеру
# quantity - кол-во по ордеру
# amount - сумма по ордеру


# Получение сделок пользователя
# Наименование метода: 	user_trades
# Тип запроса: 	POST
# Входящие параметры: 	
# pair - одна или несколько валютных пар разделенных запятой (пример BTC_USD,BTC_EUR)
# offset - смещение от последней сделки (по умолчанию 0)
# limit - кол-во возвращаемых сделок (по умолчанию 100, максимум 10 000)
# Пример использования: 	
# api_query("user_trades", Array(
#     "pair"=>"BTC_USD",
#     "limit"=>100,
#     "offset"=>0
# ));
# Возращаемое значение:
# {
#   "BTC_USD": [
#     {
#       "trade_id": 3,
#       "date": 1435488248,
#       "type": "buy",
#       "pair": "BTC_USD",
#       "order_id": 7,
#       "quantity": 1,
#       "price": 100,
#       "amount": 100
#     }
#   ]
# }
# Описание полей: 	
# trade_id - идентификатор сделки
# date - дата и время сделки
# type - тип сделки
# pair - валютная пара
# order_id - идентификатор ордера пользователя
# quantity - кол-во по сделке
# price - цена сделки
# amount - сумма сделки


# Получение отмененных ордеров пользователя
# Наименование метода: 	user_cancelled_orders
# Тип запроса: 	POST
# Входящие параметры: 	
# offset - смещение от последней сделки (по умолчанию 0)
# limit - кол-во возвращаемых сделок (по умолчанию 100, максимум 10 000)
# Пример использования: 	
# api_query("user_cancelled_orders", Array(
#     "limit"=>100,
#     "offset"=>0
# ));
# Возращаемое значение: 	
# [
#   {
#     "date": 1435519742,
#     "order_id": 15,
#     "order_type": "sell",
#     "pair": "BTC_USD",
#     "price": 100,
#     "quantity": 3,
#     "amount": 300
#   }
# ]
# Описание полей: 	
# date - дата и время отмены ордера
# order_id - идентификатор ордера
# order_type - тип ордера
# pair - валютная пара
# price - цена по ордеру
# quantity - кол-во по ордеру
# amount - сумма по ордеру


# Получение истории сделок ордера
# Наименование метода: 	order_trades
# Тип запроса: 	POST
# Входящие параметры: 	
# order_id - идентификатор ордера
# Пример использования: 	
# api_query("order_trades", Array(
#     "order_id"=>12345
# ));
# Возращаемое значение: 	
# {
#   "type": "buy",
#   "in_currency": "BTC",
#   "in_amount": "1",
#   "out_currency": "USD",
#   "out_amount": "100",
#   "trades": [
#     {
#       "trade_id": 3,
#       "date": 1435488248,
#       "type": "buy",
#       "pair": "BTC_USD",
#       "order_id": 12345,
#       "quantity": 1,
#       "price": 100,
#       "amount": 100
#     }
#   ]
# }
# Описание полей: 	
# type - тип ордера
# in_currency - валюта входящая
# in_amount - кол-во входящей валюты
# out_currency - валюта исходящая
# out_amount - кол-во исходящей валюты
# trades - массив сделок, где:
#     trade_id - идентификатор сделки
#     date - дата сделки
#     type - тип сделки
#     pair - валютная пара
#     order_id - идентификатор ордера
#     quantity - кол-во по сделке
#     price - цена по сделке
#     amount - сумма по сделке


# Подсчет в какую сумму обойдется покупка определенного кол-ва валюты по конкретной валютной паре
# Наименование метода: 	required_amount
# Тип запроса: 	POST
# Входящие параметры: 	
# pair - валютная пара
# quantity - кол-во которое необходимо купить
# Пример использования: 	
# api_query("required_amount", Array(
#     "pair"=>"BTC_USD",
#     "quantity"=>"11"
# ));
# Возращаемое значение: 	
# {
#   "quantity": 3,
#   "amount": 5,
#   "avg_price": 3.66666666
# }
# Описание полей: 	
# quantity - кол-во которое вы сможете купить
# amount - сумма на которую вы потратите на покупку
# avg_price - средняя цена покупки


# Получнение списка адресов для депозита криптовалют
# Наименование метода: 	deposit_address
# Тип запроса: 	POST
# Входящие параметры: 	отсутствуют
# Пример использования: 	
# api_query("deposit_address", Array());
# Возращаемое значение: 	
# {
#   "BTC": "16UM5DoeHkV7Eb7tMfXSuQ2ueir1yj4P7d",
#   "DOGE": "DEVfhgKErG5Nzas2FZJJH8Y8pjoLfVfWq4",
#   "LTC": "LSJFhsVJM6GCFtSgRj5hHuK9gReLhNuKFb",
#   "XRP": "rB2yjyFCoJaV8QCbj1UJzMnUnQJMrkhv3S,1234"
# }


# Создание задачи на вывод криптовалют.
# ВНИМАНИЕ!!! Эта API функция включается пользователю после запроса в техподдержку
# Наименование метода: 	withdraw_crypt
# Тип запроса: 	POST
# Входящие параметры: 	
# amount - кол-во выводимой валюты
# currency - наименование выводимой валюты
# address - адрес вывода
# invoice - дополнительный идентификатор (обязательно для XRP)
# Пример использования: 	
# api_query("withdraw_crypt", Array(
#     "amount"=>10,
#     "currency"=>"BTC",
#     "address"=>"16UM5DoeHkV7Eb7tMfXSu...",
#     "invoice"=>"1234"
# ));
# Возращаемое значение:
# {
#   "result": true,
#   "error": "",
#   "task_id": "467756"
# }
# Описание полей: 	
# result - true в случае успешного создания задачи на вывод, и false в случае ошибки
# error - содержит описание ошибки
# task_id - идентификатор задачи на вывод


# Получение ИД транзакции криптовалюты для отслеживания на blockchain
# Наименование метода: 	withdraw_get_txid
# Тип запроса: 	POST
# Входящие параметры: 	
# task_id - идентификатор задания на вывод
# Пример использования: 	
# api_query("withdraw_get_txid", Array(
#     "task_id"=>467756
# ));
# Возращаемое значение:
# {
#   "result": true,
#   "error": "",
#   "status": true,
#   "txid": "ec46f784ad976fd7f7539089d1a129fe46..."
# }
# Описание полей:
# result - true в случае успешного создания задачи на вывод, и false в случае ошибки
# error - содержит описание ошибки
# status - true если вывод уже осуществлен
# txid - идентификатор транзакции по которому можно её найти в blockchain



## EXCODE API
# Используя EXCODE API можно создавать и загружать купоны EXCODE.
# Доступ предоставляется после обращения в техподдержку.

# Создание купона EXCODE
# Наименование метода: 	excode_create
# Тип запроса: 	POST
# Входящие параметры: 	currency - наименование валюты купона
# amount - сумма на которую создается купон
# Пример использования
# api_query("excode_create", Array(
#     "currency"=>"BTC",
#     "amount"=>10
# ));
# Пример ответа:
# {
#   "result": true,
#   "error": "",
#   "task_id": "467757",
#   "code": "EX-CODE_9004_BTC7c3f8adc0b158658....",
#   "amount": "10",
#   "currency": "BTC",
#   "balances": {
#     "BTC": 940.994,
#     "USD": 949.472
#   }
# }
# Описание полей:
# result - true в случае успешного создания купона, и false в случае ошибки
# error - содержит описание ошибки
# task_id - идентификатор купона
# code - код EXCODE
# amount - сумма купона
# currency - валюта купона
# balances - баланс пользователя после создания купона


# Загрузка купона EXCODE
# Наименование метода: 	excode_load
# Входящие параметры: 	code - код купона EXCODE
# Пример использования
# api_query("excode_load", Array(
#     "code"=>"EX-CODE_9004_BTC7c3f8adc0b158658...."
# ));
# Возращаемое значение:
# {
#   "result": true,
#   "error": "",
#   "task_id": "467757",
#   "amount": "10",
#   "currency": "BTC",
#   "balances": {
#     "BTC": 950.994,
#     "USD": 949.472
#   }
# }
# Описание полей:
# result - true в случае успешной загрузки купона, и false в случае ошибки
# error - содержит описание ошибки
# task_id - идентификатор купона
# amount - сумма купона
# currency - валюта купона
# balances - баланс пользователя после загрузки купона


## WALLET API
# Этот API вызывается аналогично Authenticated API.
# Количество API вызовов ограничено 10 запросами в минуту с одного IP адреса.

# Получение истории wallet
# Наименование метода: 	wallet_history
# Тип запроса: 	POST
# Входящие параметры: 	date - дата timestamp за которую нужно получить историю (если не указан берется текущий день)
# Пример использования
# api_query("wallet_history", Array(
#     "date"=>1493998000
# ));
# Пример ответа:
# {
#   "result": true,
#   "error": "",
#   "begin": "1493942400",
#   "end": "1494028800",
#   "history": [{
#        "dt": 1461841192,
#        "type": "deposit",
#        "curr": "RUB",
#        "status": "processing",
#        "provider": "Qiwi (LA) [12345]",
#        "amount": "1",
#        "account": "",
#      },
#      {
#        "dt": 1463414785,
#        "type": "withdrawal",
#        "curr": "USD",
#        "status": "paid",
#        "provider": "EXCODE",
#        "amount": "-1",
#        "account": "EX-CODE_19371_USDda...",
#      }
#   ]
# }
# Описание полей:
# result - true в случае успешного получения истории, и false в случае ошибки
# error - содержит описание ошибки
# begin - начало периода
# end - конец периода
# history - массив операций пользователя (история кошелька), где
# dt - дата операции
# type - тип
# curr - валюта
# status - статус
# provider - провайдер
# amount - сумма
# account - счет


## Ограничение количества запросов
# Количество API вызовов ограничено 180 запросами в минуту 
# с одного IP адреса либо от одного пользователя.

