import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
from matplotlib.patches import Rectangle

from fxcharts import renko


def date_converter(sdate):
    return datetime.datetime.strptime(sdate, "%b %d %Y")


def _plot_renko(ax, bricks):
    ymax = max(bricks) + 20
    ymin = min(np.absolute(bricks)) - 20
    width = 1.0 / len(bricks)

    for index, brick in enumerate(bricks):
        if brick > 0:
            facecolor = 'green'
        else:
            facecolor = 'red'

        ypos = (abs(brick) - ymin) / (ymax - ymin)
        if index == len(bricks)-1:
            pass
        else:
            aux1 = (abs(bricks[index+1]) - ymin) / (ymax - ymin)
            height = abs(aux1 - ypos)

        rect = Rectangle((index * width, ypos), width, height,
                         facecolor=facecolor, alpha=0.5)
        ax.add_patch(rect)
    pass


if __name__ == "__main__":
    ohlc = pd.read_csv(
        "data.csv",
        sep=";",
        thousands=",",
        decimal=".",
        dtype={"open": np.float64,
               "high": np.float64,
               "low": np.float64,
               "close": np.float64,
               "volume": np.int32
               },
        converters={"date": date_converter})

    # renko with based on value
    bricks_fixed = renko(ohlc["close"], fixed=5)

    # renko with based on percentage
    bricks_percentage = renko(ohlc["close"], percentage=0.02)

    # plot candlesticks bar
    ax1 = plt.subplot(3, 1, 1)
    ohlc["date"] = ohlc["date"].apply(mdates.date2num)
    candlestick_ohlc(ax1, ohlc.values, width=0.4,
                     colorup='#77d879', colordown='#db3f3f')

    # plot renko bars
    ax2 = plt.subplot(3, 1, 2)
    _plot_renko(ax2, bricks_fixed)

    ax3 = plt.subplot(3, 1, 3)
    _plot_renko(ax3, bricks_percentage)

    plt.show()
