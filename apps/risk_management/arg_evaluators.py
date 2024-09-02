"""
A collection of argument evaluators for TA-LIB functions
"""

import typing

from apps.stocks.models import Stock, KSE100Rate
from .criteria.functions import FunctionSpec, ensure_ndarray


@ensure_ndarray(array_dtype=float)
def OPEN_VALUES(stock: Stock, /, spec: FunctionSpec) -> typing.List[float]:
    """Returns a list containing `open` values of a stock rate"""
    return stock.rates.values_list("open", flat=True)


@ensure_ndarray(array_dtype=float)
def HIGH_VALUES(stock: Stock, /, spec: FunctionSpec) -> typing.List[float]:
    """Returns a list containing `high` values of a stock rate"""
    return stock.rates.values_list("high", flat=True)


@ensure_ndarray(array_dtype=float)
def LOW_VALUES(stock: Stock, /, spec: FunctionSpec) -> typing.List[float]:
    """Returns a list containing `low` values of a stock rate"""
    return stock.rates.values_list("low", flat=True)


@ensure_ndarray(array_dtype=float)
def CLOSE_VALUES(stock: Stock, /, spec: FunctionSpec) -> typing.List[float]:
    """Returns a list containing `close` values of a stock rate"""
    return stock.rates.values_list("close", flat=True)


@ensure_ndarray(array_dtype=float)
def VOLUME_VALUES(stock: Stock, /, spec: FunctionSpec) -> typing.List[float]:
    """Returns a list containing `volume` values of a stock rate"""
    return stock.rates.values_list("volume", flat=True)


@ensure_ndarray(array_dtype=float)
def KSE100_CLOSE_VALUES(stock: Stock, /, spec: FunctionSpec) -> typing.List[float]:
    """Returns a list containing `close` values of the KSE100 rates"""
    return KSE100Rate.objects.values_list("close", flat=True)


@ensure_ndarray(array_dtype=float)
def PERIODS(stock: Stock, /, spec: FunctionSpec) -> typing.List[float]:
    """Returns a list containing `periods` values of a stock rate"""
    return 


###########
# ALIASES #
###########

Open = OPEN_VALUES
High = HIGH_VALUES
Low = LOW_VALUES
Close = CLOSE_VALUES
Volume = VOLUME_VALUES
KSE100Close = KSE100_CLOSE_VALUES
Periods = PERIODS

Real = Close
Real0 = KSE100Close
Real1 = Close
