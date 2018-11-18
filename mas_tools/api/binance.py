# -*- coding: utf-8 -*-
"""https://github.com/binance-exchange/binance-official-api-docs"""

import time
import urllib
import hmac, hashlib
import requests
from urllib.parse import urlencode

from mas_tools.api.common import BaseApi


class Binance(BaseApi):
    """Binance API"""

    server = 'https://api.binance.com/'
    methods = {
            # public methods    ## {'url': '', 'method': 'GET', 'private': False}
            'ping':             {'url': 'api/v1/ping', 'method': 'GET', 'private': False},
            'server_time':      {'url': 'api/v1/time', 'method': 'GET', 'private': False},
            'exchange_info':    {'url': 'api/v1/exchangeInfo', 'method': 'GET', 'private': False},
            'candlesticks':     {'url': 'api/v1/klines', 'method': 'GET', 'private': False},
            'orders':           {'url': 'api/v1/depth', 'method': 'GET', 'private': False, 'args': ['symbol', 'limit']},
            'tickers':          {'url': 'api/v1/depth', 'method': 'GET', 'private': False, 'args': ['symbol', 'limit']},
            'ticker_24':        {'url': 'api/v1/ticker/24hr', 'method': 'GET', 'private': False},
            'ticker_price':     {'url': 'api/v3/ticker/price', 'method': 'GET', 'private': False},
            'ticker_book_price':{'url': 'api/v3/ticker/bookTicker', 'method': 'GET', 'private': False},
            'trades':           {'url': 'api/v1/trades', 'method': 'GET', 'private': False, 'args': ['symbol', 'limit']},
            'h_trades':         {'url': 'api/v1/historicalTrades', 'method': 'GET', 'private': False},
            'aggr_trades':      {'url': 'api/v1/aggTrades', 'method': 'GET', 'private': False},
            # private methods   ## {'url': '', 'method': 'GET', 'private': True}
            'account':          {'url': 'api/v3/account', 'method': 'GET', 'private': True},
            'new_order':        {'url': 'api/v3/order', 'method': 'POST', 'private': True},
            'cancel_order':     {'url': 'api/v3/order', 'method': 'DELETE', 'private': True},
            'order_info':       {'url': 'api/v3/order', 'method': 'GET', 'private': True},
            'test_order':       {'url': 'api/v3/order/test', 'method': 'POST', 'private': True},
            'open_orders':      {'url': 'api/v3/openOrders', 'method': 'GET', 'private': True},
            'all_orders':       {'url': 'api/v3/allOrders', 'method': 'GET', 'private': True},
            'my_trades':        {'url': 'api/v3/myTrades', 'method': 'GET', 'private': True},
    }
    periods = ['1m', '3m', '5m', '15m', '30m',
                '1h', '2h', '4h', '6h', '8h', '12h',
                '1d', '3d', '1w', '1M']
    errors = {
        # 10xx - General Server or Network issues
        '-1000': 'UNKNOWN',
                    # An unknown error occured while processing the request.
        '-1001': 'DISCONNECTED',
                    # Internal error; unable to process your request. Please try again.
        '-1002': 'UNAUTHORIZED',
                    # You are not authorized to execute this request.
        '-1003': 'TOO_MANY_REQUESTS',
                    # Too many requests.
                    # Too many requests queued.
                    # Too many requests; current limit is %s requests per minute. Please use the websocket for live updates to avoid polling the API.
                    # Way too many requests; IP banned until %s. Please use the websocket for live updates to avoid bans.
        '-1006': 'UNEXPECTED_RESP',
                    # An unexpected response was received from the message bus. Execution status unknown.
        '-1007': 'TIMEOUT',
                    # Timeout waiting for response from backend server. Send status unknown; execution status unknown.
        '-1010': 'ERROR_MSG_RECEIVED',
                    # See Description
        '-1013': 'INVALID_MESSAGE',
                    # INVALID_MESSAGE
        '-1014': 'UNKNOWN_ORDER_COMPOSITION',
                    # Unsupported order combination.
        '-1015': 'TOO_MANY_ORDERS',
                    # Too many new orders.
                    # Too many new orders; current limit is %s orders per %s.
        '-1016': 'SERVICE_SHUTTING_DOWN',
                    # This service is no longer available.
        '-1020': 'UNSUPPORTED_OPERATION',
                    # This operation is not supported.
        '-1021': 'INVALID_TIMESTAMP',
                    # Timestamp for this request is outside of the recvWindow.
                    # Timestamp for this request was 1000ms ahead of the server's time.
        '-1022': 'INVALID_SIGNATURE',
                    # Signature for this request is not valid.
        # 11xx - Request issues
        '-1100': 'ILLEGAL_CHARS',
                    # Illegal characters found in a parameter.
                    # Illegal characters found in parameter '%s'; legal range is '%s'.
        '-1101': 'TOO_MANY_PARAMETERS',
                    # Too many parameters sent for this endpoint.
                    # Too many parameters; expected '%s' and received '%s'.
                    # Duplicate values for a parameter detected.
        '-1102': 'MANDATORY_PARAM_EMPTY_OR_MALFORMED',
                    # A mandatory parameter was not sent, was empty/null, or malformed.
                    # Mandatory parameter '%s' was not sent, was empty/null, or malformed.
                    # Param '%s' or '%s' must be sent, but both were empty/null!
        '-1103': 'UNKNOWN_PARAM',
                    # An unknown parameter was sent.
        '-1104': 'UNREAD_PARAMETERS',
                    # Not all sent parameters were read.
                    # Not all sent parameters were read; read '%s' parameter(s) but was sent '%s'.
        '-1105': 'PARAM_EMPTY',
                    # A parameter was empty.
                    # Parameter '%s' was was empty.
        '-1106': 'PARAM_NOT_REQUIRED',
                    # A parameter was sent when not required.
                    # Parameter '%s' sent when not required.
        '-1112': 'NO_DEPTH',
                    # No orders on book for symbol.
        '-1114': 'TIF_NOT_REQUIRED',
                    # TimeInForce parameter sent when not required.
        '-1115': 'INVALID_TIF',
                    # Invalid timeInForce.
        '-1116': 'INVALID_ORDER_TYPE',
                    # Invalid orderType.
        '-1117': 'INVALID_SIDE',
                    # Invalid side.
        '-1118': 'EMPTY_NEW_CL_ORD_ID',
                    # New client order ID was empty.
        '-1119': 'EMPTY_ORG_CL_ORD_ID',
                    # Original client order ID was empty.
        '-1120': 'BAD_INTERVAL',
                    # Invalid interval.
        '-1121': 'BAD_SYMBOL',
                    # Invalid symbol.
        '-1125': 'INVALID_LISTEN_KEY',
                    # This listenKey does not exist.
        '-1127': 'MORE_THAN_XX_HOURS',
                    # Lookup interval is too big.
                    # More than %s hours between startTime and endTime.
        '-1128': 'OPTIONAL_PARAMS_BAD_COMBO',
                    # Combination of optional parameters invalid.
        '-1130': 'INVALID_PARAMETER',
                    # Invalid data sent for a parameter.
                    # Data sent for paramter '%s' is not valid.
        # 20xx - Processing Issues
        '-2008': 'BAD_API_ID',
                    # Invalid Api-Key ID
        '-2009': 'DUPLICATE_API_KEY_DESC',
                    # API-key desc already exists.
        '-2010': 'NEW_ORDER_REJECTED',
                    # See Description
        '-2011': 'CANCEL_REJECTED',
                    # See Description
        '-2012': 'CANCEL_ALL_FAIL',
                    # Batch cancel failure.
        '-2013': 'NO_SUCH_ORDER',
                    # Order does not exist.
        '-2014': 'BAD_API_KEY_FMT',
                    # API-key format invalid.
        '-2015': 'REJECTED_MBX_KEY',
                    # Invalid API-key, IP, or permissions for action.
        # Messages for -1010, -2010, -2011
        # This code is sent when an error has been returned by the matching engine. The following messages which will indicate the specific error:
        # Error message 	Description
        # "Unknown order sent."    The order (by either orderId, clOrdId, origClOrdId) could not be found
        # "Duplicate order sent."  The clOrdId is already in use
        # "Market is closed."      The symbol is not trading
        # "Account has insufficient balance for requested action."      Not enough funds to complete the action
        # "Market orders are not supported for this symbol."            MARKET is not enabled on the symbol
        # "Iceberg orders are not supported for this symbol."           icebergQty is not enabled on the symbol
        # "Stop loss orders are not supported for this symbol."         STOP_LOSS is not enabled on the symbol
        # "Stop loss limit orders are not supported for this symbol."   STOP_LOSS_LIMIT is not enabled on the symbol
        # "Take profit orders are not supported for this symbol."       TAKE_PROFIT is not enabled on the symbol
        # "Take profit limit orders are not supported for this symbol." TAKE_PROFIT_LIMIT is not enabled on the symbol
        # "Cancel order is invalid. Check origClOrdId and orderId."     No origClOrdId or orderId was sent in.
        # "Price * QTY is zero or less."             price * quantity is too low
        # "IcebergQty exceeds QTY."                  icebergQty must be less than the order quantity
        # "This action disabled is on this account." Contact customer support; some actions have been disabled on the account.
        # "Unsupported order combination"            The orderType, timeInForce, stopPrice, and/or icebergQty combination isn't allowed.
        # "Order would trigger immediately."         The order's stop price is not valid when compared to the last traded price.
        # "Order would immediately match and take."  LIMIT_MAKER order type would immediately match and trade, and not be a pure maker order.
        # 9xxx Filter failures
        # Error message 	Description
        # "Filter failure: PRICE_FILTER"             price is too high, too low, and/or not following the tick size rule for the symbol.
        # "Filter failure: LOT_SIZE"                 quantity is too high, too low, and/or not following the step size rule for the symbol.
        # "Filter failure: MIN_NOTIONAL"             price * quantity is too low to be a valid order for the symbol.
        # "Filter failure: MAX_NUM_ORDERS"           Account has too many open orders on the symbol.
        # "Filter failure: MAX_ALGO_ORDERS"          Account has too many open stop loss and/or take profit orders on the symbol.
        # "Filter failure: EXCHANGE_MAX_NUM_ORDERS"  Account has too many open orders on the exchange.
        # "Filter failure: EXCHANGE_MAX_ALGO_ORDERS" Account has too many open stop loss and/or take profit orders on the exchange.
    }

    def call_api(self, **kwargs):
        """"""
        command = kwargs.pop('command')
        api_url = self.server + self.methods[command]['url']

        payload = kwargs
        headers = {}

        if self.methods[command]['private']:
            payload.update({'timestamp': int(time.time() + self.shift_seconds - 1) * 1000})

            sign = hmac.new(
                key=self.API_SECRET,
                msg=urllib.parse.urlencode(payload).encode('utf-8'),
                digestmod=hashlib.sha256
            ).hexdigest()

            payload.update({'signature': sign})
            headers = {"X-MBX-APIKEY": self.API_KEY}

        if self.methods[command]['method'] == 'GET':
            api_url += '?' + urllib.parse.urlencode(payload)

        response = requests.request(method=self.methods[command]['method'],
                                    url=api_url,
                                    data="" if self.methods[command]['method'] == 'GET' else payload,
                                    headers=headers)
        if 'code' in response.text:
            raise ConnectionError(response.text)
        return response.json()

