import typing

from apps.stocks.models import Stock
from criteria.functions import FunctionSpec, ArgEvaluator


def OPEN_VALUES(stock: Stock, /, spec: FunctionSpec) -> typing.List[float]:
    """Returns the open values of a stock"""
    return stock.rates.values_list("open", flat=True)


def HIGH_VALUES(stock: Stock, /, spec: FunctionSpec) -> typing.List[float]:
    """Returns the high values of a stock"""
    return stock.rates.values_list("high", flat=True)


def LOW_VALUES(stock: Stock, /, spec: FunctionSpec) -> typing.List[float]:
    """Returns the low values of a stock"""
    return stock.rates.values_list("low", flat=True)


def CLOSE_VALUES(stock: Stock, /, spec: FunctionSpec) -> typing.List[float]:
    """Returns the close values of a stock"""
    return stock.rates.values_list("close", flat=True)


def VOLUME_VALUES(stock: Stock, /, spec: FunctionSpec) -> typing.List[float]:
    """Returns the volume values of a stock"""
    return stock.rates.values_list("volume", flat=True)


Open = ArgEvaluator[Stock, typing.List[float]](OPEN_VALUES)
High = ArgEvaluator[Stock, typing.List[float]](HIGH_VALUES)
Low = ArgEvaluator[Stock, typing.List[float]](LOW_VALUES)
Close = ArgEvaluator[Stock, typing.List[float]](CLOSE_VALUES)
Volume = ArgEvaluator[Stock, typing.List[float]](VOLUME_VALUES)


