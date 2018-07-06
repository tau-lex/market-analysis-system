"""
Implementation exchange connectors and api wrapper.
"""
import logging
from abc import ABCMeta, abstractmethod, abstractproperty

import numpy as np
import pandas as pd

# import quandl
from mas_tools.api import BaseApi
from mas_tools.utils.trade import calculate_stop_loss, calculate_lot


log = logging.getLogger(__name__)


class AbstractMarket():
    """Implements the interface of the exchange wrapper."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def observation(self, row=-1):
        """Returns the state of the market at the current position.
        
        Arguments
            row (int): Row in dataset."""

        raise NotImplementedError()

    def reset(self):
        """Reset market state."""
        
        raise NotImplementedError()

    @abstractmethod
    def buy_order(self, symbol=None):
        """Implements execution of an order to purchase an asset.
        
        Arguments
            symbol (str): Symbol from the list of traded symbols."""

        raise NotImplementedError()

    @abstractmethod
    def sell_order(self, symbol):
        """Implements execution of a warrant for the sale of an asset.
        
        Arguments
            symbol (str): Symbol from the list of traded symbols."""

        raise NotImplementedError()

    @abstractproperty
    def shape(self):
        """Returns the shape of one market observation."""

        raise NotImplementedError()

    @abstractproperty
    def symbols_count(self):
        """Returns the number of traded symbols."""

        raise NotImplementedError()

    @abstractproperty
    def balance(self):
        """Returns the balance value."""

        raise NotImplementedError()

    @abstractproperty
    def deposit(self):
        """Returns the deposit value."""

        raise NotImplementedError()

    @abstractproperty
    def profit(self):
        """Returns the profit after close opened order."""

        raise NotImplementedError()

    @abstractproperty
    def done(self):
        """Returns the done work flag."""

        raise NotImplementedError()


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


class VirtualExchange(AbstractMarket):
    """
    Implement wrapper real exchange with api.
    All datas is real exchange. All operations is virtual.
    """

    __candles = True
    __volumes = False
    __tickers = True
    __trades = False

    def __init__(self, api: BaseApi, symbols=['ETHUSDT'], period='5m',
                    balance=1000.0, commission=0.001,
                    order_risk=0.02, month_risk=0.06,
                    lot_size=0.0, limit=20, **kwargs):
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
        super(VirtualExchange, self).__init__()

        self.__api = api

        if symbols is str: symbols = np.array([symbols])
        self.symbols = symbols
        self.period = period
        self.limit = limit

        self.__done = False
        self.__balance = balance + 0.0 # fix
        self.__start_balance = balance + 0.0
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
                self.__data[item['symbol']]['deposit'] = 0.0
                self.__data[item['symbol']]['buy_price'] = 0.0

    def load_data(self, limit=100):
        """Loads data of all symbols from servers or API."""

        # TODO implement multythreading
        for symbol in self.symbols:
            # TODO WARNING this data transformation is only for binance api
            if self.__candles or self.__volumes:
                candles = pd.DataFrame(
                        self.__api.candlesticks(symbol=symbol,
                                interval=self.period, limit=limit),
                        dtype=np.float)
                if self.__candles:
                    self.__data[symbol]['candles'] = candles.values[:, 1:5] # o,h,l,c
                    # log.debug('{} candles shape = {}'.format(symbol, self.__data[symbol]['candles'].shape))
                    # log.debug('{} candles = \n{}'.format(symbol, self.__data[symbol]['candles']))
                if self.__volumes:
                    self.__data[symbol]['volumes'] = np.column_stack((
                            candles.values[:, 5],     # vol
                            candles.values[:, 7],     # 7:11 = qv, nt, bv, qv
                            candles.values[:, 9:11]
                    ))
                    # log.debug('{} volumes shape = {}'.format(symbol, self.__data[symbol]['volumes'].shape))
                    # log.debug('{} volumes = \n{}'.format(symbol, self.__data[symbol]['volumes']))

            if self.__tickers:
                tickers = pd.DataFrame(self.__api.tickers(symbol=symbol, limit=limit))

                self.__data[symbol]['tickers'] = np.column_stack((
                        np.array([x[0:2] for x in tickers['bids'].values], dtype=np.float),
                        np.array([x[0:2] for x in tickers['asks'].values], dtype=np.float)
                ))
                # log.debug('{} tickers shape = {}'.format(symbol, self.__data[symbol]['tickers'].shape))
                # log.debug('{} tickers = \n{}'.format(symbol, self.__data[symbol]['tickers']))

            if self.__trades:
                trades = pd.DataFrame(
                        self.__api.aggr_trades(symbol=symbol, limit=limit),
                        dtype=np.float)
                        
                self.__data[symbol]['trades'] = np.column_stack((
                        trades[['p', 'q']].values,
                        np.zeros((limit, 2))
                ))
                # log.debug('{} trades shape = {}'.format(symbol, self.__data[symbol]['trades'].shape))
                # log.debug('{} trades = \n{}'.format(symbol, self.__data[symbol]['trades']))

        # TODO save data for training

    def observation(self):
        """Returns current exchange states."""

        log.debug('Balance: {} / start: {}'.format(self.balance, self.__start_balance))

        self.__profit = 0.0
        if self.balance <= 0.0:
            log.debug('== DONE FLAG ==')
            self.__done = True

        # TODO ?? load train data if agent.training
        self.load_data(self.limit)

        result = np.array([])

        for symbol in self.symbols:
            if self.__candles:
                result = np.append(result, self.__data[symbol]['candles'])
            if self.__volumes:
                result = np.append(result, self.__data[symbol]['volumes'])
            if self.__tickers:
                result = np.append(result, self.__data[symbol]['tickers'])
            if self.__trades:
                result = np.append(result, self.__data[symbol]['trades'])
        
        # log.debug('Observation length = {}'.format(result.shape))

        return result.reshape(self.shape)

    def reset(self):
        """Reset market state."""
        
        self.__done = False
        self.__profit = 0.0
        self.__balance = self.__start_balance + 0.0
        for symbol in self.__data.keys():
            self.__data[symbol]['deposit'] = 0.0
            self.__data[symbol]['buy_price'] = 0.0

    def buy_order(self, symbol):
        """Open buying order.

        Arguments:
            symbol (str): Name of the trading instrument.
        """
        
        # skip if you have an open order
        if self.__data[symbol]['deposit'] > 0.0:
            return

        price = float(self.__api.ticker_book_price(symbol=symbol)['askPrice'])
        stop_loss = calculate_stop_loss(self.__data[symbol]['candles'][-12:, 2], 'buy')
        
        lot_size = self.calc_order_size(symbol, price, stop_loss)
        
        amount = price * lot_size

        if amount > 0 and self.balance - amount > 0:
            self.__data[symbol]['deposit'] += lot_size
            self.__data[symbol]['buy_price'] = price
            self.__balance -= amount * (1.0 + self.__commission)
            # self.__profit = -lot_size # TODO check with him
        elif self.balance - amount <= 0:
            log.debug('Buy Error | B={} A={} L={} P={} SL={}'.format(
                        self.balance, amount, lot_size, price, stop_loss))
            self.__done = True

    def sell_order(self, symbol):
        """
        Arguments:
            symbol (str): Name of the trading instrument.
        """

        # skip if you do not have an open order
        if self.__data[symbol]['deposit'] <= 0.0:
            return
        
        price = float(self.__api.ticker_book_price(symbol=symbol)['bidPrice'])
        # stop_loss = calculate_stop_loss(self.__data[symbol]['candles'][-12:, 1], 'sell')
        
        lot_size = self.__data[symbol]['deposit']
        
        amount = price * lot_size
        
        if amount > 0 and self.__data[symbol]['deposit'] - lot_size >= 0:
            # reward = price*lot - old_price*lot
            self.__profit = amount - self.__data[symbol]['buy_price'] * self.__data[symbol]['deposit']
            # stimulus
            if self.__profit > 0:
                self.__profit += 10
            self.__data[symbol]['deposit'] -= lot_size
            self.__balance += amount * (1.0 - self.__commission)
        else:
            log.debug('Sell Error | B={} A={} L={} P={}'.format(
                        self.balance, amount, lot_size, price))

    def calc_order_size(self, symbol, price, stop):
        """Calculate lot size.
        
        Returns
            lot_size (float): Purchase order size."""

        if self.__lot_size == 0.0:
            # TODO Check calculations (stop=ok, )
            return calculate_lot(one_lot_risk=abs(price - stop),
                            balance_risk=self.balance * self.__order_risk,
                            min_lot=self.__data[symbol]['limits']['minQty'])
        elif self.__lot_size >= self.__data[symbol]['limits']['minQty']:
            return self.__lot_size
        
        return self.__data[symbol]['limits']['minQty']

    @property
    def balance(self):
        """Returns the balance value."""

        return self.__balance

    def deposit(self, symbol):
        """Returns the deposit value."""

        return self.__data[symbol]['deposit']

    @property
    def profit(self):
        """Returns the profit after close opened order."""

        return self.__profit

    @property
    def done(self):
        """Returns the done work flag."""

        return self.__done

    @property
    def shape(self):
        """Returns the data shape."""

        columns = (4 if self.__candles else 0) + \
                  (4 if self.__volumes else 0) + \
                  (4 if self.__tickers else 0) + \
                  (4 if self.__trades else 0)

        return (len(self.symbols),  # Symbols count.
                self.limit,         # Length arrays.
                columns             # Sum columns (candles(5+4), tickers(2+2), trades(2))
               )
    
    @property
    def symbols_count(self):
        """Returns the number of traded symbols."""

        return len(self.symbols)
    
    def __len__(self):
        return self.limit


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
