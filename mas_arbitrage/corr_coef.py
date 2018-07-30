import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mas_tools.api import Binance

from scipy.stats.stats import pearsonr


def pearsonr2(x, y):
    """"""

    assert len(x) == len(y)

    n = len(x)
    sum_x = float(sum(x))
    sum_y = float(sum(y))
    sum_x_sq = sum(map(lambda k: pow(k, 2), x))
    sum_y_sq = sum(map(lambda k: pow(k, 2), y))
    sum_p = sum(map(lambda k, l: k * l, x, y))
    num = sum_p - (sum_x * sum_y/n)
    den = pow((sum_x_sq - pow(sum_x, 2) / n) * (sum_y_sq - pow(sum_y, 2) / n), 0.5)

    if den == 0:
        return 0

    return num / den


api = Binance('', '')

# 1m, 3m, 5m, 15m, 30m
# 1h, 2h, 4h, 6h, 8h
# 12h, 1d, 3d, 1w, 1M
period = '5m'
limit = 1000

btc = pd.DataFrame(
        api.candlesticks(symbol='BTCUSDT',
                interval=period, limit=limit),
        dtype=np.float)

eth = pd.DataFrame(
        api.candlesticks(symbol='ETHUSDT',
                interval=period, limit=limit),
        dtype=np.float)

x = btc[4].values
y = eth[4].values

corr1 = pearsonr(x, y)
corr2 = np.corrcoef(x, y)
corr3 = pearsonr2(x, y)
print('\nscipy corr = {}\nnumpy corr = {}\ncustum corr = {}\n'.format(corr1, corr2, corr3))

z = x - y
plt.plot(z)
# for i in zones:
#     plt.axhline(y=i, color='grey', linestyle='--')
plt.show()
