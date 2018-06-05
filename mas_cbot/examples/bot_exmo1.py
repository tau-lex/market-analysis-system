#'Exbot'
#'(C) Nov-2016 ob1kenobi'
#'Donate BTC: 16mSMKbNNpEJc1GasDb1JN5FzNnNYCgpdy'

#Импорт библиотек
import httplib
import urllib
import urllib2
import json
import hashlib
import hmac
import time
import copy
import string
import random
import socket
import sys


#описание переменных
nonce_last=1
cons=0


#описание констант
BTC_ak=['']
BTC_as=['']





def reset_con():
    global cons

    url="api.exmo.me"
    
    try:
        cons.close()
    except:
        print '~',

    try:
        cons = httplib.HTTPSConnection(url, timeout=10)
    except:
        print '~',
        
    return




def get_depth(pairs_url):


    url='/v1/order_book/?pair='+pairs_url.upper()+'&limit=200'
    headers = { "Content-type": "application/x-www-form-urlencoded", 'User-Agent' : 'bot17'}

    cons.request("GET", url, None, headers)
    response = cons.getresponse()
    y=json.load(response)

    z={}
    for p in y:
        p2=p.lower()
            
        z[p2]={'asks':[], 'bids':[]}
        for q in y[p]['ask']:
            z[p2]['asks'].append([float(q[0]), float(q[1])])
        for q in y[p]['bid']:
            z[p2]['bids'].append([float(q[0]), float(q[1])])
                    
    return z
    
        




def get_status(ind_ak=0):

    global nonce_last


    try:
        nonce = int(time.time()*10-14830000000)
        nonce=max(nonce, nonce_last+1)
        nonce_last=nonce

        params = {"nonce": nonce}
        params = urllib.urlencode(params)

        H = hmac.new(BTC_as[0], digestmod=hashlib.sha512)
        H.update(params)
        sign = H.hexdigest()

        headers = {"Content-type": "application/x-www-form-urlencoded",
                           "Key":BTC_ak[0],
                           "Sign":sign,
                           'User-Agent' : 'bot1'}
        cons.request("POST", "/v1/user_info", params, headers)
        response = cons.getresponse()

        a = json.load(response)
        z={}
        z['return']={}
        z['return']['funds']={}
        for m in a['balances']:
            p2=m.lower()
            z['return']['funds'][p2] = float(a['balances'][m])
        
    except:
        reset_con()
        return 0

    return z






def get_my_orders(ind_ak=0):

    global nonce_last


    try:
        nonce = int(time.time()*10-14830000000)
        nonce=max(nonce, nonce_last+1)
        nonce_last=nonce

        params = {"nonce": nonce}
        params = urllib.urlencode(params)

        H = hmac.new(BTC_as[0], digestmod=hashlib.sha512)
        H.update(params)
        sign = H.hexdigest()

        headers = {"Content-type": "application/x-www-form-urlencoded",
                           "Key":BTC_ak[0],
                           "Sign":sign,
                           'User-Agent' : 'bot1'}
        cons.request("POST", "/v1/user_open_orders", params, headers)
        response = cons.getresponse()

        a = json.load(response)
        #print 'get_my_orders'
        #print a
        z={}
        z['success']=0
        z['error']='all ok'
        z['return']={}
        for p in a:
            for j in range(len(a[p])):
                z['success']=1
                oid=a[p][j]["order_id"]
                
                p2=a[p][j]["pair"].lower()
                    
                z['return'][oid]={"pair":p2, "type":a[p][j]["type"],
                                  "amount":float(a[p][j]["quantity"]), "rate":float(a[p][j]["price"])}
                
        if z['success']==0:
            z['error']='no orders'
        
    except:
        print '!1',
        reset_con()
        return 0

    return z



def cancel_order(ord, ind_ak=0):

    global nonce_last


    try:
        nonce = int(time.time()*10-14830000000)
        nonce=max(nonce, nonce_last+1)
        nonce_last=nonce

        params = {"nonce": nonce, "order_id":ord}
        params = urllib.urlencode(params)

        H = hmac.new(BTC_as[0], digestmod=hashlib.sha512)
        H.update(params)
        sign = H.hexdigest()

        headers = {"Content-type": "application/x-www-form-urlencoded",
                           "Key":BTC_ak[0],
                           "Sign":sign,
                           'User-Agent' : 'bot1'}
        cons.request("POST", "/v1/order_cancel", params, headers)
        response = cons.getresponse()

        a = json.load(response)
        
    except:
        reset_con()
        return 0

    return a




def trade(ord_type, ord_rate, ord_amount, p, ind_ak=0):

    global nonce_last


    try:
        nonce = int(time.time()*10-14830000000)
        nonce=max(nonce, nonce_last+1)
        nonce_last=nonce

        params = {"nonce": nonce, "pair":p.upper(), 'quantity':ord_amount, 'price':ord_rate, 'type':ord_type}
        params = urllib.urlencode(params)

        H = hmac.new(BTC_as[0], digestmod=hashlib.sha512)
        H.update(params)
        sign = H.hexdigest()

        headers = {"Content-type": "application/x-www-form-urlencoded",
                           "Key":BTC_ak[0],
                           "Sign":sign,
                           'User-Agent' : 'bot1'}
        cons.request("POST", "/v1/order_create", params, headers)
        response = cons.getresponse()

        a = json.load(response)
        if a['error']!='':
            print 'Trade: ', a['error']
            
        aa=a['order_id']
        return aa
        
    except:
        print 'Tr!',
        reset_con()
        return 0





def find_rate(depth, pair, typ, am_lim):
    rate=depth[pair][typ][0][0]
    am_sum=0.0
    for orders in depth[pair][typ]:
        am=orders[1]
        rate=orders[0]
        am_sum += am
        if am_sum>=am_lim:
            break

    return rate    



#функция bot(pair=пара, sp_lim1=0.4%, sp_lim2=1%, sp_cancel=0.6%)
#am_min=?
#round_rate
#am_lim=0.25
#rate_min_step=0.001 (function of round_rate)
def bot(pair, sp_lim1=0.4, sp_lim2=1, sp_cancel=0.6, am_min=0.01, round_rate=3, am_lim=0.25):


    rate_min_step=pow(10.0, -round_rate)
    mm=pair.split('_')
    m1=mm[0]
    m2=mm[1]

    reset_con()

    loop_cnt=100500

    #бесконечный цикл:
    while True:
        try:
            loop_cnt += 1
            

            #задержка чтоб не превысить лимит обращений по АПИ
            time.sleep(1.0)

            #запросить стакан
            depth=get_depth(pair)

            rate_avg=(depth[pair]['asks'][0][0]+depth[pair]['bids'][0][0])*0.5

            ##spread=вычислить_спред()
            spread=abs(depth[pair]['asks'][0][0]-depth[pair]['bids'][0][0])/rate_avg

            #запросить остатки валют
            balance=get_status()

            #запросить мои ордера
            my_orders=get_my_orders()

            if loop_cnt>60:
                bb=copy.deepcopy(balance)
                if my_orders['success']==0 and my_orders['error']=='no orders':
                    dummy=1
                else:
                    for order in my_orders['return']:
                        o=my_orders['return'][order]
                        if o['pair'] != pair:
                            continue
                        mm=o['pair'].split('_')
                        if o['type'] == 'sell':
                            v=mm[0]
                            am=o['amount']
                        elif o['type'] == 'buy':
                            v=mm[1]
                            am=o['amount']*o['rate']
                        else:
                            print '!1',
                            break

                        bb['return']['funds'][v] += float(am)


                print
                print m1, '=', bb['return']['funds'][m1], ' ',
                print m2, '=', bb['return']['funds'][m2]
                print 'total', m1, '=', bb['return']['funds'][m1] + bb['return']['funds'][m2]/rate_avg, ' ',
                print 'total', m2, '=', bb['return']['funds'][m2] + bb['return']['funds'][m1]*rate_avg
                loop_cnt = 0
                

    ##		цикл по моим ордерам:
    ##			если ордер на продажу И курс>средний курс+sp_cancel:
    ##				отменить ордер
    ##			иначе если ордер на покупку И курс<средний курс- sp_cancel:
    ##				отменить ордер

            c1=find_rate(depth, pair, 'asks', am_lim)
            c2=find_rate(depth, pair, 'bids', am_lim)
            was_cancel=0
            if my_orders['success']==0 and my_orders['error']=='no orders':
                dummy=1
            else:
                for order in my_orders['return']:
                    o=my_orders['return'][order]
                    if o['pair'] != pair:
                        continue
                    if o['type'] == 'sell' and (o['rate']>rate_avg*(1.0+sp_cancel*0.01) or o['rate']>=c1):
                        print
                        print 'cancel', order, o['type'], o['amount'], 'rate=', o['rate']
                        cancel_order(order)
                        was_cancel=1
                    elif o['type'] == 'buy'  and (o['rate']<rate_avg/(1.0+sp_cancel*0.01) or o['rate']<=c2):
                        print
                        print 'cancel', order, o['type'], o['amount'], 'rate=', o['rate']
                        cancel_order(order)
                        was_cancel=1

    ##		если была отмена ордера:
    ##			перейти на начало цикла
            if was_cancel==1:
                loop_cnt=100500
                continue
    ##
    ##		если на остатках валюты нет:
    ##			напечатать '-'
    ##			перейти на начало цикла
            print '-',
            if balance['return']['funds'][m1]<am_min and balance['return']['funds'][m2]/rate_avg < am_min*1.02:
                continue

            
    ##
    ##
    ##		если на остатках есть 2-я валюта пары (баксы при паре бтц/усд):
    ##			если spread>sp_lim2:
    ##				с=вычислить_средний_курс()-0,5%
    ##				выставить_ордер(покупка, курс=c, обьем=вся 2-я валюта)
    ##				напечатать инфу об ордере и остатки в валютах
    ##			иначе если spread<sp_lim1:
    ##				c1=найти_курс(продажа, 0.25btc)/1.004
    ##				c2=найти_курс(покупка, 0.25btc)+0.001
    ##				c=min(c1,c2)
    ##				выставить_ордер(покупка, курс=c, обьем=вся 2-я валюта)
    ##				напечатать инфу об ордере и остатки в валютах
    ##			иначе (если спред больше 0.4%):
    ##				c=найти_курс(покупка, 0.25btc)+0.001
    ##				выставить_ордер(покупка, курс=c, обьем=вся 2-я валюта)
    ##				напечатать инфу об ордере и остатки в валютах


            if balance['return']['funds'][m2]/rate_avg > am_min*1.02:
                loop_cnt = 100500
                if spread>(sp_lim2*0.01):
                    c=round(rate_avg/1.005, round_rate) #<--- 1.005
                    trade('buy', c, balance['return']['funds'][m2]/c*0.99999, pair)   #need round for c
                    print
                    print 'spread(%)=',round(spread*100.0, 2),'>sp_lim2'
                    print 'buy by rate', c,' ', balance['return']['funds'][m2], m2
                elif spread<(sp_lim1*0.01):
                    c1=find_rate(depth, pair, 'asks', am_lim)/1.004 # change to bid/ask
                    c2=find_rate(depth, pair, 'bids', am_lim)+rate_min_step
                    c=round(min(c1, c2), round_rate)
                    trade('buy', c, balance['return']['funds'][m2]/c*0.99999, pair)   #need round for c
                    print
                    print 'spread(%)=',round(spread*100.0, 2),'<sp_lim1'
                    print 'buy by rate', c,' ', balance['return']['funds'][m2], m2
                else:
                    c=find_rate(depth, pair, 'bids', am_lim)+rate_min_step
                    c=round(c, round_rate)
                    trade('buy', c, balance['return']['funds'][m2]/c*0.99999, pair)   #need round for c
                    print
                    print 'spread(%)=',round(spread*100.0, 2),' else '
                    print 'buy by rate', c,' ', balance['return']['funds'][m2], m2
                    
    ##
    ##		если на остатках есть 1-я валюта пары (битки при паре бтц/усд):
    ##			если spread>sp_lim2:
    ##				с=вычислить_средний_курс()+0,5%
    ##				выставить_ордер(продажа, курс=c, обьем=вся 1-я валюта)
    ##				напечатать инфу об ордере и остатки в валютах
    ##			иначе если spread<sp_lim1:
    ##				c1=найти_курс(покупка, 0.25btc)*1.004
    ##				c2=найти_курс(продажа, 0.25btc)-0.001
    ##				c=max(c1,c2)
    ##				выставить_ордер(продажа, курс=c, обьем=вся 1-я валюта)
    ##				напечатать инфу об ордере и остатки в валютах
    ##			иначе (если спред больше 0.4%):
    ##				c2=найти_курс(продажа, 0.25btc)-0.001
    ##				выставить_ордер(продажа, курс=c, обьем=вся 1-я валюта)
    ##				напечатать инфу об ордере и остатки в валютах
            if balance['return']['funds'][m1]>=am_min:
                loop_cnt = 100500
                if spread>(sp_lim2*0.01):
                    c=round(rate_avg*1.005, round_rate)
                    trade('sell', c, balance['return']['funds'][m1], pair)   #need round for c
                    print
                    print 'spread(%)=',round(spread*100.0, 2),'>sp_lim2'
                    print 'sell by rate', c,' ', balance['return']['funds'][m1], m1
                elif spread<(sp_lim1*0.01):
                    c1=find_rate(depth, pair, 'bids', am_lim)*1.004 # change to bid/ask
                    c2=find_rate(depth, pair, 'asks', am_lim)-rate_min_step
                    c=round(max(c1, c2), round_rate)
                    trade('sell', c, balance['return']['funds'][m1], pair)   #need round for c
                    print
                    print 'spread(%)=',round(spread*100.0, 2),'<sp_lim1'
                    print 'sell by rate', c,' ', balance['return']['funds'][m1], m1
                else:
                    c=find_rate(depth, pair, 'asks', am_lim)-rate_min_step
                    c=round(c, round_rate)
                    trade('sell', c, balance['return']['funds'][m1], pair)   #need round for c
                    print
                    print 'spread(%)=',round(spread*100.0, 2),' else '
                    print 'sell by rate', c,' ', balance['return']['funds'][m1], m1
        except:
            print '*',
            reset_con()
            time.sleep(5)


