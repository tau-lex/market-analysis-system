import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging

from mas_tools.api import Binance
from mas_tools.trade import calculate_cointegration_scores


path = 'E:/Projects/market-analysis-system/mas_arbitrage/'
logging.basicConfig(level=logging.INFO,
                    handlers=[logging.FileHandler("{p}/{fn}.log".format(p=path, fn='bot_0.0')),
                                logging.StreamHandler()]
                    )
log = logging.getLogger()

api = Binance('', '')

# 1m, 3m, 5m, 15m, 30m
# 1h, 2h, 4h, 6h, 8h
# 12h, 1d, 3d, 1w, 1M
period = '1h'
limit = 1000
base = 'BTCUSDT'
# pairs = ['ETHUSDT', 'BNBUSDT', 'BCCUSDT', 'EOSUSDT', 'ADAUSDT', 'LTCUSDT', 'NEOUSDT', 'XLMUSDT', 'XRPUSDT']
pairs = ['BCCUSDT']

symb1 = pd.DataFrame(
        api.candlesticks(symbol=base,
                interval=period, limit=limit),
        dtype=np.float)
x = symb1[4].values

for pair in pairs:
    try:
        print('{}\n{} vs {} ({}):'.format(40*'=', base, pair, period))
        symb2 = pd.DataFrame(
                api.candlesticks(symbol=pair,
                        interval=period, limit=limit),
                dtype=np.float)
        y = symb2[4].values

        fn = path + base + '-' + pair + '_' + period
        calculate_cointegration_scores(x, y, plot_graph=True, save_graph_path=fn)
    except ValueError:
        pass

