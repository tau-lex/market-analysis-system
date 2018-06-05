# -*- coding: utf-8 -*-
"""
Implementation exchange connectors and api wrapper.
"""

import time
from math import floor

import numpy as np
import pandas as pd

import quandl
from mas_tools.api import BaseApi


class AbstractMarket():
    """Implement Base class exchange wrapper."""
    
    # __df = pd.DataFrame([])
    # __data = np.array([])
    symbols = np.array([])
    periods = np.array([])

    __balance = 0.0
    __balance_fd = 0.0
    __balance_ut = 0
    __deposit = 0.0

    def __init__(self, api: BaseApi, symbols=['ETHUSDT'], periods=['1h'],
                    balance=1000.0, order_risk=0.02, month_risk=0.06,
                    lot_size=1, **kwargs):
        """Constructor.
        
        Arguments:
            api (BaseApi): 
            symbols (str or list):
            periods (str or list):
            balance (float):
            order_risk (float[0.0-1.0]):
            month_risk:
            lot_size:
        """
        self.__api = api

        if symbols is str: symbols = np.array([symbols])
        if periods is str: periods = np.array([periods])
        self.symbols = symbols
        self.periods = periods
        
        self.__balance = balance
        self.__start_balance = self.balance

        assert (0.0 <= order_risk <= 1.0) or (0.0 <= month_risk <= 1.0), 'The risk must have a value from zero to one.'

        self.__ex_info = self.__api.exchange_info()

        self.__order_risk = order_risk
        self.__month_risk = month_risk
        for item in self.__ex_info['symbols']:
            if item['symbol'] == self.symbols[0]:
                self.__step_price = float(item['filters'][0]['tickSize'])
                self.__min_lot = float(item['filters'][1]['minQty'])
                self.__step_lot = float(item['filters'][1]['minQty'])
                self.__min_amount = float(item['filters'][2]['minNotional'])
                break
        
        self.__lot_size = lot_size

        self.load_data()

    def load_data(self):
        """Loads data of all symbols from servers or API."""
        
        self.__df = pd.DataFrame(self.__api.candlesticks(symbol=self.symbols[0],
                                                           interval=self.periods[0]),
                                    dtype=np.float)
        self.__data = self.__df.values
        # self.__data = quandl.get('GDAX/ETH_USD')

    def observation(self, row, size):
        """"""

        return self.__data[row-size: row, :]

    def calculate_amount(self, price):
        """"""

        amount = price * self.__lot_size

        # one_lot_risk = abs(price - self.calculate_stop_loss(data[?], ))
        # self.calculate_lot(one_lot_risk)

        return amount

    def buy_order(self, price, lot=1.0):
        """"""

        amount = self.calculate_amount(price)

        if amount > 0 and self.__balance - amount >= 0:
                self.__deposit += lot
                self.__balance -= amount

    def sell_order(self, price, lot=1.0):
        """"""

        amount = self.calculate_amount(price)
        
        if amount > 0 and self.__deposit - lot >= 0:
            self.__deposit -= lot
            self.__balance += amount

    def reset(self):
        """Reset market state."""
        
        self.__balance = self.__start_balance
        self.__deposit = 0.0

    @staticmethod
    def calculate_lot(self, one_lot_risk, min_lot=0.0):
        """Calculate lot size with risk value.
        
        Arguments:
            one_lot_risk:
            min_lot:
        """

        if min_lot == 0.0:
            min_lot = self.__min_amount
        if one_lot_risk * min_lot >= self.__order_risk or one_lot_risk <= 0:
            return min_lot
        elif min_lot == 1:
            return floor(self.__order_risk / one_lot_risk) # Часть от риска лотом
        else:
            return round(self.__order_risk / one_lot_risk - min_lot, 2)
        return -1.0

    def calculate_stop_loss(self, data, side):
        """Calculates the stop level of the input array of prices.

        The minimum number of prices is 10 last candles in front of the bar
        being calculated. The method is described by Alexander Elder.

        # Arguments
            data (arraylike): an array of prices, the size of (n, 1) or (n, 4),
                    where n is greater than or equal to 10.
            side (str): direction, 'buy' / 'sale', 'up' / 'down'.
        # Returns
            stop_price (float): The price of the breakdown in the opposite direction,
            at which it is necessary to close the position.
        """

        lst1 = ['buy', 'up']
        lst2 = ['sell', 'down']
        if side not in lst1 or side not in lst2:
            raise ValueError("Illegal argument side")
        if len(data) < 10:
            raise ValueError()
        # TODO
        stop_price = 0.0

        return stop_price

    @property
    def balance(self):
        """Returns the balance value."""
        return self.__balance

    @property
    def balance_fd(self):
        """Returns the balance value of the first day of the month."""
        return self.__balance_fd

    def __len__(self):
        return len(self.__data)
        
    @staticmethod
    def adjust_to_step(self, value, step, increase=False):
        """Rounds any number to a multiple of the specified step.

        from: https://bablofil.ru

        Arguments:
            increase (bool): if True - rounding will occur to a larger step value.
        """
        return ((int(value * 100000000) - int(value * 100000000) % int(
                float(step) * 100000000)) / 100000000)+(float(step) if increase else 0)


class VirtualMarket(AbstractMarket):
    """
    Implement wrapper real exchange with api.
    All datas is real exchange. All operations is virtual.
    """
    
    def __init__(self, commission=0.001, *args, **kwargs):
        """"""
        super(VirtualMarket, self, args, kwargs)
        self.__commission = commission

class RealExchange(AbstractMarket):
    """
    Implement wrapper real exchange with api.
    """
    pass
