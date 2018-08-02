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
db_url = 'postgres://postgres:postgres@localhost/postgres'
experiments, steps, model_params = labnotebook.initialize(db_url)

# cripto exchange api
MY_API_KEY = '---'
MY_API_SECRET = '---'
api = Binance(MY_API_KEY, MY_API_SECRET)

# parameters
symb1 = 'BTCUSDT'
symb2 = 'BCCUSDT'
period = '1m'
arbitrage_sum = True
eps, mu, std = 0., 0., 0.
limit = 1000

stop_size = 0.8 # of zones
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
zones = [-2., 0., 2.]
stops = [zones[0] - stop_size, zones[2] + stop_size]
opened_orders = []
history = []
out_of_stop = False

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
                            interval=period, limit=limit),
                    dtype=np.float)[4].values
            y = pd.DataFrame(
                    api.candlesticks(symbol=symb2,
                            interval=period, limit=limit),
                    dtype=np.float)[4].values
            eps, mu, std = calculate_cointegration_scores(x, y)

        # Update prices
        new_prices = {symb1: float(api.ticker_price(symbol=symb1)['price']),
                      symb2: float(api.ticker_price(symbol=symb2)['price'])}

        z_score = (new_prices[symb1] - eps * new_prices[symb2] - mu) / std
        past_z_score = (past_prices[symb1] - eps * past_prices[symb2] - mu) / std

        # Check stop levels
        if stops[1] <= z_score or z_score <= stops[0]:
            out_of_stop = True
        if out_of_stop:
            # raise ValueError('Out of z-score range!')
            # TODO close orders
            pass

        # trades
        zone_level = check_touch_of_zone(zones, z_score, past_z_score)
        if zone_level != 0:
            # middles zones level
            zlen = len(zones)
            mid = int(zlen / 2) if zlen % 2 == 0 else int(zlen / 2) + 1

            # skip
            if len(opened_orders) >= max_orders:
                continue

            # check opened orders
            if zone_level == mid:
                # close opened
                for order in opened_orders:
                    open_order(-(order - mid))
                    opened_orders.remove(order)
                    history.append([time(), z_score])
            elif zone_level != mid:
                # open order
                open_order(zone_level - mid)
                opened_orders.append(zone_level)
                history.append([time(), z_score])

        balance['sum'] = new_prices[symb1]*balance[symb1] + new_prices[symb2]*balance[symb2] + balance['usd']
        log.info('Tick: {t}\nBalances: {b:0.6f} BTC, {e:0.6f} ETH, {u:0.2f} USD\nSum balance: {s:0.2f} USD\nLevels of opened orders: {o}'.format(
                t=tick_count, b=balance[symb1], e=balance[symb2],
                u=balance['usd'], s=balance['sum'], o=opened_orders
        ))
        
        # labnotebook
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
labnotebook.end_experiment(experiment, final_trainacc=balance['sum'])
