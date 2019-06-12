import math
import numpy as np


def renko(ds, **kwargs):
    """
    Creates Renko chart bars from a iterable data array.
    
    Input:
        kwargs: the possible args are the following:
            fixed: creates the renko chart with a fixed brick size
    
    Return: an array with renko levels. The levels can be negative or positive.
        A positive level indicates a green candle and the negative value indicates 
        a red candle. The values are the bottom of the renko candles.
    """
    if not hasattr(ds, "__iter__"):
        raise Exception("Not iterable object")

    if "fixed" in kwargs:
        return _renko_step(ds, kwargs["fixed"])
    elif "percentage" in kwargs:
        return _renko_percentage(ds, kwargs["percentage"])

    raise ValueError("Not recognized method")


def _renko_step(ds, step):
    chart = []
    last_price = ds[0]
    for price in ds:
        bricks = math.floor(abs(price-last_price)/step)
        if bricks == 0:
            continue

        sign = int(np.sign(price-last_price))
        chart += [sign*(last_price+(sign*step*x)) for x in range(1, bricks+1)]
        last_price = abs(chart[-1])
    return chart


def _renko_percentage(ds, percentage):
    chart = []
    last_price = ds[0]
    for price in ds:
        inc = (price-last_price)/last_price
        if abs(inc) < percentage:
            continue

        sign = int(np.sign(price-last_price))
        bricks = math.floor(inc/percentage)
        step = math.floor((percentage * (price-last_price)) / inc)
        chart += [sign*(last_price+(sign*step*x))
                  for x in range(1, abs(bricks)+1)]
        last_price = abs(chart[-1])
    return chart
