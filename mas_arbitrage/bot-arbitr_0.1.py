from time import sleep, time
import logging
import numpy as np
import pandas as pd

import labnotebook
from mas_tools.api import Binance
from mas_tools.trade import calculate_cointegration_scores


# logging
path = 'E:/Projects/market-analysis-system/mas_arbitrage/'
logging.basicConfig(level=logging.INFO,
                    handlers=[logging.FileHandler("{p}/{fn}.log".format(p=path, fn='bot_0.1')),
                                logging.StreamHandler()]
                    )
log = logging.getLogger()

# labnotebook
labnotebook_flag = False
if labnotebook_flag:
    db_url = 'postgres://postgres:postgres@localhost/postgres'
    experiments, steps, model_params = labnotebook.initialize(db_url)

# cripto exchange api
MY_API_KEY = '---'
MY_API_SECRET = '---'
api = Binance(MY_API_KEY, MY_API_SECRET)

# parameters
symb1 = 'BTCUSDT'
symb2 = 'BCCUSDT'
calc_period = '5m'
period = '1m'
arbitrage_sum = True
eps, mu, std = 0., 0., 0.
limit = 1000

stop_size = 0.8 # of levels
max_orders = 4
fees = 0.005

start_usd = 300
balance = {
    symb1: 1 / float(api.ticker_price(symbol=symb1)['price']) * start_usd,
    symb2: 1 / float(api.ticker_price(symbol=symb2)['price']) * start_usd,
    'usd': start_usd,
    'sum': 0.0
}
lot = {
    symb1: balance[symb1]*0.1,
    symb2: balance[symb2]*0.1,
    'usd': balance['usd']*0.1
}

tick_count = 0
levels = [-2., 0., 2.]
stops = [levels[0] - stop_size, levels[2] + stop_size]
opened_orders = []
history = []
stop_flag = False

# functions
def check_touch_of_zone(levels, new_price, old_price):
    """Checks the touch by the price of the boundaries of the zone.
    
    Arguments
        levels (list): List of separation levels.
        new_price (int or float): Current price.
        old_price (int or float): Previous price.
        
    Returns
        index (int): Zone boundary index. Positive index - breakup, negative - breakdown."""

    length = len(levels)
    for idx in range(length):
        if new_price >= old_price:
            if old_price <= levels[idx] and levels[idx] <= new_price:
                return levels[idx] # breakup
        else:
            if new_price <= levels[idx] and levels[idx] <= old_price:
                return -levels[idx] # breakdown

    return None

def buy(symbol):
    """"""
    price = float(api.ticker_book_price(symbol=symbol)['askPrice'])
    # float(api.ticker_price(symbol=symb1)['price'])
    
    lot_size = lot[symbol]
    
    amount = price * lot_size #* (1.0 + fees)

    if amount > 0 and balance['usd'] - amount > 0:
        balance[symbol] += lot_size
        balance['usd'] -= amount
        # self.__profit = -lot_size # TODO check with him
    else:
        print('Buy Error | B={} A={} L={} P={}'.format(
                balance['usd'], amount, lot_size, price))

def sell(symbol):
    """"""
    price = float(api.ticker_book_price(symbol=symbol)['bidPrice'])
    
    lot_size = lot[symbol]
    
    amount = price * lot_size #* (1.0 - fees)
    
    if amount > 0 and balance[symbol] - lot_size >= 0:
        balance[symbol] -= lot_size
        balance['usd'] += amount
    else:
        print('Sell Error | B={} A={} L={} P={}'.format(
                balance[symbol], amount, lot_size, price))

def open_order(zone_index):
    """"""
    if arbitrage_sum:
        if zone_index >= 0:
            sell(symb1)
            buy(symb2)
        else:
            buy(symb1)
            sell(symb2)
    else:
        if zone_index >= 0:
            sell(symb1)
            sell(symb2)
        else:
            buy(symb1)
            buy(symb2)

# pre start
past_prices = {symb1: float(api.ticker_price(symbol=symb1)['price']),
               symb2: float(api.ticker_price(symbol=symb2)['price'])}

balance['sum'] = past_prices[symb1]*balance[symb1] + past_prices[symb2]*balance[symb2] + balance['usd']
log.info('Start balance: {b:0.2f} USD'.format(b=balance['sum']))

# labnotebook
if labnotebook_flag:
    model_desc = {'pair_1': symb1, 'pair_2': symb2,
                    'period': period,
                    symb1: balance[symb1], symb2: balance[symb2],
                    'USD': balance['usd'], 'sum_balance': balance['sum'],
                    'stop_size': stop_size}
    experiment = labnotebook.start_experiment(model_desc=model_desc)

while True:
    try:
        sleep(30)
        # update coefficients
        if tick_count % 100000 == 0:
            x = pd.DataFrame(
                    api.candlesticks(symbol=symb1,
                            interval=calc_period, limit=limit),
                    dtype=np.float)[4].values
            y = pd.DataFrame(
                    api.candlesticks(symbol=symb2,
                            interval=calc_period, limit=limit),
                    dtype=np.float)[4].values
            eps, mu, std = calculate_cointegration_scores(x, y)

        # Update prices
        new_prices = {symb1: float(api.ticker_price(symbol=symb1)['price']),
                      symb2: float(api.ticker_price(symbol=symb2)['price'])}
        if arbitrage_sum:
            z_score = (new_prices[symb1] - eps * new_prices[symb2] - mu) / std
            past_z_score = (past_prices[symb1] - eps * past_prices[symb2] - mu) / std
        else:
            # or?
            z_score = (new_prices[symb1] - eps * new_prices[symb2] - mu) / std
            past_z_score = (past_prices[symb1] - eps * past_prices[symb2] - mu) / std

        # Check stop levels
        if z_score <= min(stops) or max(stops) <= z_score:
            if not stop_flag:
                log.info('Stop loss.')

            stop_flag = True
        else:
            stop_flag = False

        # trades
        touched_level = check_touch_of_zone(levels, z_score, past_z_score)
        if touched_level and touched_level != 0:
            # check opened orders
            if len(opened_orders) == 0:
                open_order(touched_level)
                opened_orders.append(touched_level)
                # history.append([time(), z_score])
        elif touched_level == 0:
            for order in opened_orders:
                open_order(-order)
                opened_orders.remove(order)
                # history.append([time(), z_score])

        # end tick
        balance['sum'] = new_prices[symb1]*balance[symb1] + new_prices[symb2]*balance[symb2] + balance['usd']
        log.info('Tick: {t}\nBalances: {bs1:0.6f} {s1}, {bs2:0.6f} {s2}, {u:0.2f} USD\nSum balance: {s:0.2f} USD\nLevels of opened orders: {o}'.format(
                t=tick_count, bs1=balance[symb1], bs2=balance[symb2],
                s1=symb1[:3], s2=symb2[:3],
                u=balance['usd'], s=balance['sum'], o=opened_orders
        ))
        
        # labnotebook
        if labnotebook_flag:
            labnotebook.step_experiment(experiment,
                                        timestep=tick_count,
                                        trainacc=balance['sum'],
                                        custom_fields={symb1: balance[symb1], symb2: balance[symb2],
                                                        'USD': balance['usd'], 'sum_balance': balance['sum']})
            
        past_prices = new_prices
        tick_count += 1

    except RuntimeError:
        pass


log.info('======== End program ========\nFinal balance: {} USD'.format(balance['sum']))
np.savetxt(path+'history.csv', np.array(history), fmt='%.2f', delimiter=';')
# we close the experiment and pass all final indicators:
if labnotebook_flag:
    labnotebook.end_experiment(experiment, final_trainacc=balance['sum'])
