# -*- coding: utf-8 -*-
"""
Implementation exchange connectors and api wrapper.
"""
from math import floor

import numpy as np
import pandas as pd

# import quandl
from mas_tools.api import BaseApi
from mas_tools.tools import calculate_stop_loss, calculate_lot


#=============================================================================#
#                                                                             #
#=============================================================================#
class AbstractMarket():
    """Implements the interface of the exchange wrapper."""

    __balance = 0.0
    __profit = 0.0      # current reward
    __balance_fd = 0.0  # the first day of the month
    __balance_ut = 0    # date of the last update of the balance_fd
    __done = False      # flag end of the dataset

    def observation(self, row=-1):
        """Returns the state of the market at the current position.
        
        # Arguments
            row (int): Row in dataset."""

        raise NotImplementedError()

    def reset(self):
        """Reset market state."""
        
        self.__done = False
        self.__balance = 0.0
        self.__profit = 0.0 
        self.__balance_fd = 0.0
        self.__balance_ut = 0

    def buy_order(self, symbol=None):
        """Implements execution of an order to purchase an asset.
        
        # Arguments
            symbol (str): Symbol from the list of traded symbols."""

        raise NotImplementedError()

    def sell_order(self, symbol):
        """Implements execution of a warrant for the sale of an asset.
        
        # Arguments
            symbol (str): Symbol from the list of traded symbols."""

        raise NotImplementedError()

    @property
    def shape(self):
        """Returns the shape of one market observation."""

        raise NotImplementedError()

    @property
    def symbols_count(self):
        """Returns the number of traded symbols."""

        raise NotImplementedError()

    @property
    def balance(self):
        """Returns the balance value."""

        return self.__balance

    @property
    def balance_fd(self):
        """Returns the balance value of the first day of the month."""

        return self.__balance_fd

    @property
    def profit(self):
        """Returns the profit after close opened order."""

        return self.__profit

    @property
    def done(self):
        """Returns the done work flag."""

        return self.__done


#=============================================================================#
#                                                                             #
#=============================================================================#
class VirtualMarket(AbstractMarket):
    """Implements access to the abstract market."""

    def __init__(self, api: BaseApi, symbols=['ETHUSDT'], period='1d',
                    balance=1000.0, order_risk=0.02, month_risk=0.06,
                    window=1, lot_size=0.1, **kwargs):
        """Constructor.
        
        Arguments:
            api: Exchange connector.
            symbols (str or list):
            period (str):
            window (int):
            balance (float): Start balance.
            order_risk (float[0.0-1.0]):
            month_risk:
            lot_size:
        """
        self.__api = api

        if symbols is str: symbols = np.array([symbols])
        self.symbols = symbols
        self.period = period
        self.__position = 0
        self.__window = window
        self.__done = False
        self.__balance = balance
        self.__start_balance = self.__balance
        self.__deposit = dict(zip(symbols, [0.0 for i in symbols]))

        assert (0.0 <= order_risk <= 1.0) or (0.0 <= month_risk <= 1.0), 'The risk must have a value from zero to one.'
        self.__order_risk = order_risk
        self.__month_risk = month_risk
        self.__lot_size = lot_size

        __ex_info = self.__api.exchange_info()
        for item in __ex_info['symbols']:
            if item['symbol'] == self.symbols[0]:
                self.__step_price = float(item['filters'][0]['tickSize'])
                self.__min_lot = float(item['filters'][1]['minQty'])
                self.__step_lot = float(item['filters'][1]['minQty'])
                self.__min_amount = float(item['filters'][2]['minNotional'])
                break

    def load_data(self, limit=500):
        """Loads data of all symbols from servers or API."""
        
        # self.__data = quandl.get('GDAX/ETH_USD')
        self.__df = pd.DataFrame(self.__api.candlesticks(symbol=self.symbols[0],
                                                         interval=self.period),
                                 dtype=np.float)
        data = self.__df.values
        self.__data = np.column_stack((data[:, 1:6], data[:, 7:11]))

    def observation(self, row=-1):
        """Returns the state of the market at the current position.
        
        # Arguments
            row (int): Row in dataset."""

        self.__profit = 0.0
        if row < 0:
            row = self.__position
            self.__position += 1
        
        if row + self.__window - 1 > len(self.__data):
            raise ValueError('Out of range')

        if row + self.__window - 1 >= len(self.__data) - 1:
            self.__done = True

        return self.__data[row: row + self.__window, :]

    def reset(self):
        """Reset market state."""

        self.load_data()
        
        self.__done = False
        self.__position = 0
        self.__balance = self.__start_balance
        for depo in self.__deposit.keys:
            self.__deposit[depo] = 0.0

    def buy_order(self, symbol):
        """Implements execution of an order to purchase an asset.
        
        # Arguments
            symbol (str): Symbol from the list of traded symbols."""
    
        # [:, 0:3] = ohlc
        price = self.__data[self.__position + self.__window - 1, 0]

        amount = price * self.__lot_size
        
        if amount > 0 and self.__balance - amount > 0:
            self.__deposit += self.__lot_size
            self.__balance -= amount
            # self.__profit = -amount # TODO check with him
        elif self.__balance - amount <= 0:
            self.__done = True
        else:
            raise Exception('wtf')

    def sell_order(self, symbol):
        """Implements execution of a warrant for the sale of an asset.
        
        # Arguments
            symbol (str): Symbol from the list of traded symbols."""

        # [:, 0:3] = ohlc
        price = self.__data[self.__position + self.__window - 1, 0]

        amount = price * self.__lot_size
        
        if amount > 0 and self.__deposit - self.__lot_size >= 0:
            self.__deposit -= self.__lot_size
            self.__balance += amount
            self.__profit = amount
        else:
            raise Exception('wtf')

    @property
    def shape(self):
        """Returns the shape of one market observation."""
        
        return (self.__window, self.__data.shape[1])

    @property
    def symbols_count(self):
        """Returns the number of traded symbols."""

        return len(self.symbols)


#=============================================================================#
#                                                                             #
#=============================================================================#
class VirtualExchange(AbstractMarket):
    """
    Implement wrapper real exchange with api.
    All datas is real exchange. All operations is virtual.
    """

    __candles = True
    __tickers = True
    __trades = False

    def __init__(self, api: BaseApi, symbols=['ETHUSDT'], period='5m',
                    balance=1000.0, commission=0.001,
                    order_risk=0.02, month_risk=0.06,
                    lot_size=0.0, limit=50, **kwargs):
        """Constructor.
        
        Arguments:
            api (BaseApi): Exchange connector.
            symbols (str or list):
            period (str):
            balance (float): Start balance.
            commission (float):
            order_risk (float[0.0-1.0]):
            month_risk (float[0.0-1.0]):
            lot_size (float): The size of the new order. If zero, it will be
                                calculated on the size of risk.
        """
        super(VirtualMarket, self).__init__(api, **kwargs)

        self.__api = api

        if symbols is str: symbols = np.array([symbols])
        self.symbols = symbols
        self.period = period
        self.limit = limit

        self.__done = False
        self.__balance = balance
        self.__start_balance = self.__balance
        self.__deposit = dict(zip(symbols, [0.0, ]))
        self.__commission = commission

        assert (0.0 <= order_risk <= 1.0) or (0.0 <= month_risk <= 1.0), 'The risk must have a value from zero to one.'
        self.__order_risk = order_risk
        self.__month_risk = month_risk
        self.__lot_size = lot_size

        self.__data = dict(zip(self.symbols, [dict() for i in self.symbols]))

        ex_info = self.__api.exchange_info()
        for item in ex_info['symbols']:
            if item['symbol'] in self.symbols:
                self.__data[item['symbol']]['tradeOn'] = True if item['status'] == 'TRADING' else False
                self.__data[item['symbol']]['basePrecition'] = int(item['baseAssetPrecision'])
                self.__data[item['symbol']]['quotePrecition'] = int(item['quotePrecision'])
                tmp = {'priceStep': float(item['filters'][0]['tickSize']),
                       'minQty': float(item['filters'][1]['minQty']),
                       'qtyStep': float(item['filters'][1]['stepSize']),
                       'minOrderPrice': float(item['filters'][2]['minNotional'])}
                self.__data[item['symbol']]['limits'] = tmp

    def load_data(self, limit=100):
        """Loads data of all symbols from servers or API."""

        candles = pd.DataFrame([])
        tickers = pd.DataFrame([])
        trades = pd.DataFrame([])
        # TODO implement multythreading
        for symbol in self.symbols:
            try:
                if self.__candles:
                    candles = pd.DataFrame(self.__api.candlesticks(symbol=symbol,
                                                                   interval=self.period,
                                                                   limit=limit),
                                           dtype=np.float)
                if self.__tickers:
                    tickers = pd.DataFrame(self.__api.tickers(symbol=symbol, limit=limit))
                if self.__trades:
                    trades = pd.DataFrame(self.__api.aggr_trades(symbol=symbol, limit=limit),
                                          dtype=np.float)
            except Exception as e:
                # TODO implement response error handler
                print('error:', e)

            if self.__candles:
                self.__data[symbol]['candles'] = np.column_stack((candles.values[:, 1:6], # o,h,l,c,v
                                                                  candles.values[:, 7:11])) # qv, nt, bv, qv
            if self.__tickers:
                self.__data[symbol]['tickers'] = np.column_stack(([np.array([x[0:2] for x in tickers['bids'].values], dtype=np.float),
                                                                   np.array([x[0:2] for x in tickers['asks'].values], dtype=np.float)]))
            if self.__trades:
                self.__data[symbol]['trades'] = trades[['p', 'q']].values

        # TODO save data for training

    def observation(self):
        """Returns current exchange states."""

        self.__profit = 0.0
        if self.__balance <= 0.0:
            self.__done = True

        # TODO load train data if agent.training
        self.load_data(self.limit)

        result = np.array([])

        for symbol in self.symbols:
            sym_data = []
            if self.__candles:
                sym_data.append(self.__data[symbol]['candles'])
            if self.__tickers:
                sym_data.append(self.__data[symbol]['tickers'])
            if self.__trades:
                sym_data.append(self.__data[symbol]['trades'])
            result = np.append(result, np.column_stack(sym_data))
        
        return result.reshape(self.shape)

    def reset(self):
        """Reset market state."""
        
        self.__done = False
        self.__balance = self.__start_balance
        for depo in self.__deposit.keys():
            self.__deposit[depo] = 0.0

    def buy_order(self, symbol):
        """Open buying order.

        Arguments:
            symbol (str): Name of the trading instrument.
        """
        
        price = float(self.__api.ticker_book_price(symbol=symbol)['askPrice'])
        stop_loss = calculate_stop_loss(self.__data[symbol]['candles'][-12:, 2], 'buy')
        
        if self.__lot_size == 0.0:
            # TODO Check calculations (stop=ok, )
            lot_size = calculate_lot(one_lot_risk=abs(price - stop_loss),
                                     balance_risk=self.balance * self.__order_risk,
                                     min_lot=self.__data[symbol]['limits']['minQty'])
            if lot_size <= 0.0:
                raise Exception('The lot size can not be less than or equal to zero. Lot='+str(lot_size))
        else:
            if self.__lot_size >= self.__data[symbol]['limits']['minQty']:
                lot_size = self.__lot_size
            else:
                lot_size = self.__data[symbol]['limits']['minQty']

        amount = price * lot_size

        if amount > 0 and self.__balance - amount > 0:
            print('check')
            self.__deposit[symbol] += lot_size
            self.__balance -= amount * (1.0 + self.__commission)
            # self.__profit = -amount # TODO check with him
        elif self.__balance - amount <= 0:
            raise RuntimeError('wtf_buy :: b=%.1f a=%.1f p=%.2f l=%f sl=%.2f' \
                                % (self.__balance, amount, price, lot_size, stop_loss))
            # self.__done = True
        else:
            raise Exception('wtf')

    def sell_order(self, symbol):
        """
        Arguments:
            symbol (str): Name of the trading instrument.
        """

        price = float(self.__api.ticker_book_price(symbol=symbol)['bidPrice'])
        stop_loss = calculate_stop_loss(self.__data[symbol]['candles'][-12:, 1], 'sell')
        
        if self.__lot_size == 0.0:
            lot_size = calculate_lot(one_lot_risk=abs(price - stop_loss),
                                     balance_risk=self.balance * self.__order_risk,
                                     min_lot=self.__data[symbol]['limits']['minQty'])
            if lot_size <= 0.0:
                raise Exception('The lot size can not be less than or equal to zero. Lot='+str(lot_size))
        else:
            if self.__lot_size >= self.__data[symbol]['limits']['minQty']:
                lot_size = self.__lot_size
            else:
                lot_size = self.__data[symbol]['limits']['minQty']
        
        amount = price * lot_size
        
        if amount > 0 and self.__deposit - lot_size >= 0:
            self.__deposit -= lot_size
            self.__balance += amount * (1.0 - self.__commission)
            self.__profit = amount # reward
        else:
            raise Exception('wtf')

    @property
    def shape(self):
        """Returns the data shape."""

        columns = (9 if self.__candles else 0) + \
                  (4 if self.__tickers else 0) + \
                  (2 if self.__trades else 0)

        return (len(self.symbols),  # Symbols count.
                self.limit,         # Length arrays.
                columns             # Sum columns (candles(5+4), tickers(2+2), trades(2))
               )
    
    @property
    def shapes_of_datasets(self):
        """Returns the datasets shapes."""

        result = list()

        if self.__candles:
            result.append(9)
            # result.append(5)
        if self.__tickers:
            result.append(4)
        if self.__trades:
            result.append(2)
        
        return tuple(result)

    def __len__(self):
        return self.limit


#=============================================================================#
#                                                                             #
#=============================================================================#
class RealExchange(VirtualExchange):
    """
    Implement wrapper real exchange with api.
    """
    pass

    @property
    def balance(self):
        """Returns the balance value."""
        # TODO
        return self.__api.account()
