from time import sleep
import logging

from mas_tools.api import Binance


MY_API_KEY = '---'
MY_API_SECRET = '---'
path = 'E:/Projects/market-analysis-system/mas_arbitrage/'

logging.basicConfig(level=logging.INFO,
                    handlers=[logging.FileHandler("{p}/{fn}.log".format(p=path, fn='bot_0.0')),
                                logging.StreamHandler()]
                    )
log = logging.getLogger()

api = Binance('', '')

symb1 = 'BTCUSDT'
symb2 = 'ETHUSDT'
period = '1m'
arb_sum = True

balance = {symb1: 0.04, # ~ $330
           symb2: 0.7,  # ~ $330
           'usd': 330
}
# 0.1 of the start balance
lot = {symb1: 0.004,
       symb2: 0.07,
       'usd': 33
}

h_level = 7810
l_level = 7625
nb_zones = 12

stop_size = 0.8 # zones
max_orders = 4
opened_orders = []
out_of_stop = False

fees = 0.005

def calculate_zones(high, low, nb, stops=0.):
    """Calculate levels for channel statistic arbitrage.
    
    Arguments
        high (int, float): High level of channel.
        low (int, float): Low level of channel.
        nb (int): Number of zones in channel.
        
    Returns
        zone_levels (list): List of zones levels."""

    delta = (high - low) / nb

    zone_levels = []
    for i in range(nb+1):
        level = low + i * delta
        zone_levels.append(level)

    if stops:
        return zone_levels, (zone_levels[0] - delta * stops,
                             zone_levels[nb] + delta * stops)
    return zone_levels

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
                return idx # breakup
        else:
            if new_price <= levels[idx] and levels[idx] <= old_price:
                return -idx # breakdown

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
    if zone_index >= 0:
        sell(symb1)
        buy(symb2)
    else:
        buy(symb1)
        sell(symb2)

zones, stops = calculate_zones(h_level, l_level, nb_zones, stop_size)

past_prices = {symb1: float(api.ticker_price(symbol=symb1)['price']),
               symb2: float(api.ticker_price(symbol=symb2)['price'])}

calc = past_prices[symb1]*balance[symb1] + past_prices[symb2]*balance[symb2] + balance['usd']
log.info('Start balance: {b:0.2f} USD'.format(b=calc))

while True:
    try:
        sleep(30)

        # Update prices
        new_prices = {symb1: float(api.ticker_price(symbol=symb1)['price']),
                      symb2: float(api.ticker_price(symbol=symb2)['price'])}

        past_base = past_prices[symb1] - past_prices[symb2]
        new_base = new_prices[symb1] - new_prices[symb2]

        # Check stop levels
        if out_of_stop:
            raise ValueError('Out of base range!')
        if new_base <= stops[0] or stops[1] <= new_base:
            out_of_stop = True
            continue

        # trades
        zone_level = check_touch_of_zone(zones, new_base, past_base)
        if zone_level:
            # middles zones level
            zlen = len(zones)
            mid = int(zlen / 2) if zlen % 2 == 0 else int(zlen / 2) + 1

            # check opened orders
            for order in opened_orders: # TODO check work
                if (order >= mid and mid > zone_level) or \
                    (order < mid and mid <= zone_level):
                        open_order(zone_level - mid)
                        opened_orders.remove(order)
                        opened_orders.append(zone_level)

            if len(opened_orders) == 0: # TODO check
                open_order(zone_level - mid)

            # if len(opened_orders) >= max_orders:
            #     continue

        past_prices = new_prices
        calc = new_prices[symb1]*balance[symb1] + new_prices[symb2]*balance[symb2] + balance['usd']
        log.info('Balances: {b:0.6f} BTC, {e:0.6f} ETH, {u:0.2f} USD\nCalculated balance: {c:0.2f} USD\nLevels of opened orders: {o}'.format(
                b=balance[symb1], e=balance[symb2], u=balance['usd'], c=calc, o=opened_orders
        ))
        print(opened_orders)

    except RuntimeError:
        pass

