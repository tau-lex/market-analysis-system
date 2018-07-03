# -*- coding: utf-8 -*-
"""Exchanges API's base class.

idea from: https://bablofil.ru
"""

class BaseApi():
    """Exchanges API's base class."""

    server = 'https://127.0.0.1/'
    methods = {
            # public methods    ## {'url': '', 'method': 'GET', 'private': False, 'args': []}
            'ping':             {},
            'server_time':      {},
            'exchange_info':    {},
            'candlesticks':     {},
            'tickers':          {},
            'ticker_24':        {},
            'ticker_price':     {},
            'ticker_book_price':{},
            'trades':           {},
            'h_trades':         {},
            'agr_trades':       {},
            # private methods   ## {'url': '', 'method': 'GET', 'private': True, 'args': []}
            'account':          {},
            'new_order':        {},
            'cancel_order':     {},
            'order_info':       {},
            'test_order':       {},
            'open_orders':      {},
            'all_orders':       {},
            'my_trades':        {},
    }
    periods = []

    def __init__(self, API_KEY, API_SECRET):
        """Constructor
        
        Arguments:
            API_KEY: 
            API_SECRET:
        """

        self.API_KEY = API_KEY
        self.API_SECRET = bytearray(API_SECRET, encoding='utf-8')
        self.shift_seconds = 0

    def set_shift_seconds(self, seconds):
        """"""
        self.shift_seconds = seconds

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            kwargs.update(command=name)
            return self.call_api(**kwargs)
        return wrapper

    def call_api(self, **kwargs):
        """"""
        # command = kwargs.pop('command')
        # api_url = self.server + self.methods[command]['url']

        # payload = kwargs
        # headers = {}
        raise NotImplementedError()

