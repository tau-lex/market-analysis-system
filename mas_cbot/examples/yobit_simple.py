import os
import sys
import json
import requests
import urllib, http.client
import hmac, hashlib
import time

# Вписываем свои ключи
API_KEY = '' 
API_SECRET = b''

# Тонкая настройка
CURRENCY_1 = 'liza' 
CURRENCY_2 = 'rur'

ORDER_LIFE_TIME = 3 # через сколько минут отменять неисполненный ордер на покупку CURRENCY_1
STOCK_FEE = 0.002 # Комиссия, которую берет биржа (0.002 = 0.2%)
OFFERS_AMOUNT = 1 # Сколько предложений из стакана берем для расчета средней цены
CAN_SPEND = 100 # Сколько тратить CURRENCY_2 каждый раз при покупке CURRENCY_1 (100р в моем случае)
PROFIT_MARKUP = 0.001 # Какой навар нужен с каждой сделки? (0.001 = 0.1%)
DEBUG = True # True - выводить отладочную информацию, False - писать как можно меньше


CURR_PAIR = CURRENCY_1.lower() + "_" + CURRENCY_2.lower()
"""
    Каждый новый запрос к серверу должен содержать увеличенное число в диапазоне 1-2147483646
    Поэтому храним число в файле поблизости, каждый раз обновляя его
"""
nonce_file = "./nonce"
if not os.path.exists(nonce_file):
    with open(nonce_file, "w") as out:
        out.write('1')

# Будем перехватывать все сообщения об ошибках с биржи
class ScriptError(Exception):
    pass
class ScriptQuitCondition(Exception):
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
    conn = http.client.HTTPSConnection("yobit.io", timeout=60)
    conn.request("POST", "/tapi/", payload, headers)
    response = conn.getresponse().read()
    
    conn.close()

    try:
        obj = json.loads(response.decode('utf-8'))

        if 'error' in obj and obj['error']:
            raise ScriptError(obj['error'])
        return obj
    except json.decoder.JSONDecodeError:
        raise ScriptError('Ошибка анализа возвращаемых данных, получена строка', response)


def wanna_get():
    return  (CAN_SPEND*(1+STOCK_FEE) + CAN_SPEND * PROFIT_MARKUP) / (1 - STOCK_FEE)  # сколько хотим получить за наше кол-во

# Реализация алгоритма
def main_flow():
    
    try:
        # Получаем список активных ордеров
        opened_orders = []
        try:
            yobit_orders = call_api(method="ActiveOrders", pair=CURR_PAIR)['return']
            
            for order in yobit_orders:
                o = yobit_orders[order]
                o['order_id']=order
                opened_orders.append(o)
                
        except KeyError:
            if DEBUG:
                print('Открытых ордеров нет')

    
        sell_orders = []
        # Есть ли неисполненные ордера на продажу CURRENCY_1?
        for order in opened_orders:
            if order['type'] == 'sell':
                # Есть неисполненные ордера на продажу CURRENCY_1, выход
                raise ScriptQuitCondition('Выход, ждем пока не исполнятся/закроются все ордера на продажу (один ордер может быть разбит биржей на несколько и исполняться частями)')
            else:
                # Запоминаем ордера на покупку CURRENCY_1
                sell_orders.append(order)
                
        # Проверяем, есть ли открытые ордера на покупку CURRENCY_1
        if sell_orders: # открытые ордера есть
            for order in sell_orders:
                # Проверяем, есть ли частично исполненные
                if DEBUG:
                    print('Проверяем, что происходит с отложенным ордером', order['order_id'])
                # Получаем состояние ордера, если он еще не исполнен, отменяем
                order_info = call_api(method="OrderInfo", order_id=order['order_id'])['return'][str(order['order_id'])]
                

                if order_info ['status'] == 0 and order_info['start_amount'] == order_info['amount']: # ордер не исполнен, по нему ничего не куплено
                    time_passed = time.time()  - int(order['timestamp_created'])

                    if time_passed > ORDER_LIFE_TIME * 60:
                        # Ордер уже давно висит, никому не нужен, отменяем
                        call_api(method="CancelOrder", order_id=order['order_id']) 
                        raise ScriptQuitCondition('Отменяем ордер: за ' + str(ORDER_LIFE_TIME) + ' минут не удалось купить '+ str(CURRENCY_1))
                    else:
                        raise ScriptQuitCondition('Выход, продолжаем надеяться купить валюту по указанному ранее курсу, со времени создания ордера прошло %s секунд' % str(time_passed))
                else:
                    raise ScriptQuitCondition('Ордер на покупку открыт, по нему были торги, ждем' + str(order_info))
                   
        else: # Открытых ордеров нет
            balances = call_api(method="getInfo")['return']['funds']
            if float(balances.get(CURRENCY_1, 0)) > 0: # Есть ли в наличии CURRENCY_1, которую можно продать?
                """
                    Высчитываем курс для продажи.
                    Нам надо продать всю валюту, которую купили, на сумму, за которую купили + немного навара и минус комиссия биржи
                    При этом важный момент, что валюты у нас меньше, чем купили - бирже ушла комиссия
                    0.00134345 1.5045
                    Поэтому курс продажи может получиться довольно высоким
                """
                print('sell', balances[CURRENCY_1], wanna_get(), (wanna_get()/float(balances[CURRENCY_1])))
                new_order = call_api(method="Trade", pair=CURR_PAIR, type="sell", rate="{rate:0.8f}".format(rate=wanna_get()/float(balances[CURRENCY_1])), amount="{amount:0.8f}".format(amount=balances[CURRENCY_1]))['return']
               
                print(new_order)
                if DEBUG:
                    print('Создан ордер на продажу', CURRENCY_1, new_order['order_id'])
            else:
                # CURRENCY_1 нет, надо докупить
                # Достаточно ли денег на балансе в валюте CURRENCY_2 (Баланс >= CAN_SPEND)
                if float(balances.get(CURRENCY_2, 0)) >= CAN_SPEND:
                    # Получаем информацию по предложениям из стакана
                    offers = json.loads(requests.get("https://yobit.io/api/3/depth/"+CURR_PAIR+"?limit="+str(OFFERS_AMOUNT)).text)[CURR_PAIR]
                    prices = [bid[0] for bid in offers['bids']]                    
                    try:        
                        avg_price = sum(prices)/len(prices)
                        """
                            Посчитать, сколько валюты CURRENCY_1 можно купить.
                            На сумму CAN_SPEND за минусом STOCK_FEE, и с учетом PROFIT_MARKUP
                            ( = ниже средней цены рынка, с учетом комиссии и желаемого профита)
                        """
                        # Купить как есть, потом продать с учетом комиссии
                        my_need_price = avg_price# - avg_price * (STOCK_FEE+PROFIT_MARKUP) 
                        my_amount = CAN_SPEND/my_need_price
                        
                        print('buy: кол-во {amount:0.8f}, курс: {rate:0.8f}'.format(amount=my_amount, rate=my_need_price))
                        
                        # Допускается ли покупка такого кол-ва валюты (т.е. не нарушается минимальная сумма сделки)
                        new_order = call_api(method="Trade", pair=CURR_PAIR, type="buy", rate="{rate:0.8f}".format(rate=my_need_price), amount="{amount:0.8f}".format(amount=my_amount))['return']
                       
                        print(new_order)
                        if DEBUG:
                            print('Создан ордер на покупку', new_order['order_id'])
                            
                        
                    except ZeroDivisionError:
                        print('Не удается вычислить среднюю цену', prices)
                else:
                    raise ScriptQuitCondition('Выход, не хватает денег')
        
    except ScriptError as e:
        print(e)
    except ScriptQuitCondition as e:
        print(e)
    except Exception as e:
        print("!!!!",e)

try:
    alt_balance = call_api(method="getInfo")['return']['funds'].get(CURRENCY_1.lower(),0)
    if alt_balance > 0:
        decision = input("""
            У вас на балансе есть {amount:0.8f} {curr1}
            Вы действительно хотите, что бы бот продал все это по курсу {rate:0.8f}, выручив {wanna_get:0.8f} {curr2}?
            Введите Д/Y или Н/N
        """.format(
            amount=alt_balance,
            curr1=CURRENCY_1,
            curr2=CURRENCY_2,
            wanna_get=wanna_get(),
            rate=wanna_get()/alt_balance
        ))
        if decision in ('N','n','Н','н'):
            print("Тогда избавьтесь от {curr} и перезапустите бота".format(curr=CURRENCY_1))
            sys.exit(0)
except Exception as e:
    print(str(e))
       
while(True):
    main_flow()
    time.sleep(1)

