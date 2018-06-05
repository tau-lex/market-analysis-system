import os
import json
# import requests
import urllib, http.client
import hmac, hashlib

# Вписываем свои ключи
API_KEY = '' 
API_SECRET = b''

"""
    Каждый новый запрос к серверу должен содержать увеличенное число в диапазоне 1-2147483646
    Поэтому храним число в файле поблизости, каждый раз обновляя его
"""
nonce_file = "./nonce"
if not os.path.exists(nonce_file):
    with open(nonce_file, "w") as out:
        out.write('1')

# Будем перехватывать все сообщения об ошибках с биржи
class YobitException(Exception):
    pass
        
def call_api(**kwargs):

    # При каждом обращении к торговому API увеличиваем счетчик nonce на единицу
    with open(nonce_file, 'r+') as inp:
        nonce = int(inp.read())
        inp.seek(0)
        inp.write(str(nonce+1))
        inp.truncate()

    payload = {'nonce': nonce}

    if kwargs:
        payload.update(kwargs)
    payload =  urllib.parse.urlencode(payload)

    H = hmac.new(key=API_SECRET, digestmod=hashlib.sha512)
    H.update(payload.encode('utf-8'))
    sign = H.hexdigest()
    
    headers = {"Content-type": "application/x-www-form-urlencoded",
           "Key":API_KEY,
           "Sign":sign}
    conn = http.client.HTTPSConnection("yobit.net", timeout=60)
    conn.request("POST", "/tapi/", payload, headers)
    response = conn.getresponse().read()
    
    conn.close()

    try:
        obj = json.loads(response.decode('utf-8'))

        if 'error' in obj and obj['error']:
            raise YobitException(obj['error'])
        return obj
    except json.decoder.JSONDecodeError:
        raise YobitException('Ошибка анализа возвращаемых данных, получена строка', response)

print ('Получаем информацию по аккаунту', '*'*30)
print( call_api(method="getInfo") )

try:
    print ('Создаем ордер на покупку', '*'*30)
    print( call_api(method="Trade", pair="ltc_btc", type="buy", rate="0.1", amount=0.01) )
except YobitException as e:
    print("Облом:", e)

try:
    print ('Создаем ордер на продажу', '*'*30)
    print( call_api(method="Trade", pair="ltc_btc", type="sell", rate="0.1", amount=0.01) )
except YobitException as e:
    print("Облом:", e)

try:
    print ('Получаем список активных ордеров', '*'*30)
    print( call_api(method="ActiveOrders", pair="ltc_btc") )
except YobitException as e:
    print("Облом:", e)

try:
    print ('Получаем информацию по ордеру', '*'*30)
    print( call_api(method="OrderInfo", order_id="123") )
except YobitException as e:
    print("Облом:", e)

try:
    print ('Отменяем ордер', '*'*30)
    print( call_api(method="CancelOrder", order_id="123") )
except YobitException as e:
    print("Облом:", e)

try:
    print ('Получаем историю торгов', '*'*30)
    print( call_api(method="TradeHistory", pair="ltc_btc") )
except YobitException as e:
    print("Облом:", e)

try:
    print ('Получаем кошель для пополнения (BTC)', '*'*30)
    print( call_api(method="GetDepositAddress", coinName="BTC") )
except YobitException as e:
    print("Облом:", e)

