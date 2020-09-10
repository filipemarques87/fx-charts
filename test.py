import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
from matplotlib.patches import Rectangle

from fxcharts import renko, ha_candlesticks


def date_converter(sdate):
    return datetime.datetime.strptime(sdate, "%b %d %Y")


def _plot_renko(ax, bricks):
    ymax = max(bricks) + 20
    ymin = min(np.absolute(bricks)) - 20
    width = 1.0 / len(bricks)

    prev_height = 0
    for index, brick in enumerate(bricks):
        if brick > 0:
            facecolor = 'green'
        else:
            facecolor = 'red'

        ypos = (abs(brick) - ymin) / (ymax - ymin)
        if index == len(bricks)-1:
            pass
        elif bricks[index] == bricks[index+1]:
            height = prev_height
        else:
            aux1 = (abs(bricks[index+1]) - ymin) / (ymax - ymin)
            height = abs(aux1 - ypos)
            prev_height = height

        rect = Rectangle((index * width, ypos), width, height,
                         facecolor=facecolor, alpha=0.5)
        ax.add_patch(rect)
    pass


def _plot_renko2(ax, ohlc):
    width = 1
    width2 = 0.1
    pricesup = ohlc[ohlc.close >= ohlc.open]
    pricesdown = ohlc[ohlc.close < ohlc.open]

    ax.bar(pricesup.index, pricesup.close-pricesup.open,
           width, bottom=pricesup.open, color='g')
    ax.bar(pricesup.index, pricesup.high-pricesup.close,
           width2, bottom=pricesup.close, color='g')
    ax.bar(pricesup.index, pricesup.low-pricesup.open,
           width2, bottom=pricesup.open, color='g')

    ax.bar(pricesdown.index, pricesdown.close-pricesdown.open,
           width, bottom=pricesdown.open, color='r')
    ax.bar(pricesdown.index, pricesdown.high-pricesdown.open,
           width2, bottom=pricesdown.open, color='r')
    ax.bar(pricesdown.index, pricesdown.low-pricesdown.close,
           width2, bottom=pricesdown.close, color='r')

    # ax.grid()


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

    ohlc["date"] = ohlc["date"].apply(mdates.date2num)

    # renko with based on value
    bricks_fixed = renko(ohlc["close"], fixed=5)

    # renko with based on percentage
    bricks_percentage = renko(ohlc["close"], percentage=0.02, condensed=False)

    # renko with based on atr
    bricks_atr = renko(ohlc, atr=30, condensed=False)

    # # compute the haiken ashi bars
    # ha_bars = ha_candlesticks(ohlc)

    # RENKO CHART
    fig1 = plt.figure()
    # plot candlesticks chart
    ax1 = plt.subplot(4, 1, 1)
    ax1.margins(0)
    candlestick_ohlc(ax1, ohlc.values, width=0.4,
                     colorup='#77d879', colordown='#db3f3f')

    # plot renko charts
    ax2 = plt.subplot(4, 1, 2)
    pd_fixed = pd.DataFrame.from_dict(bricks_fixed)
    _plot_renko2(ax2, pd_fixed)
    # candlestick_ohlc(ax2, pd_fixed.values, width=0.4,
    #                  colorup='#77d879', colordown='#db3f3f')

    ax3 = plt.subplot(4, 1, 3)
    pd_percentage = pd.DataFrame.from_dict(bricks_percentage)
    _plot_renko2(ax3, pd_percentage)
    # candlestick_ohlc(ax3, pd_percentage.values, width=0.4,
    #                  colorup='#77d879', colordown='#db3f3f')

    ax4 = plt.subplot(4, 1, 4)
    pd_atr = pd.DataFrame.from_dict(bricks_atr)
    _plot_renko2(ax4, pd_atr)
    # candlestick_ohlc(ax4, pd_atr.values, width=0.4,
    #                  colorup='#77d879', colordown='#db3f3f')

    # HEIKIN ASHI CHART
    # fig2 = plt.figure()
    # # plot candlesticks chart
    # ax1 = plt.subplot(2, 1, 1)
    # candlestick_ohlc(ax1, ohlc.values, width=0.4,
    #                  colorup='#77d879', colordown='#db3f3f')

    # # plot heikei ashi chart
    # # data must be in format: (t, open, high, low, close), ...
    # ha_cs = []
    # for i in range(len(ha_bars["open"])):
    #     ha_cs.append((ohlc["date"][i], ha_bars["open"][i],
    #                   ha_bars["high"][i], ha_bars["low"][i], ha_bars["close"][i]))

    # ax2 = plt.subplot(2, 1, 2)
    # candlestick_ohlc(ax2, ha_cs, width=0.4,
    #                  colorup='#77d879', colordown='#db3f3f')

    
    plt.show()
    # fig1.savefig("sample_renko.png",  dpi=fig1.dpi)
    # fig2.savefig("sample_ha.png",  dpi=fig2.dpi)
