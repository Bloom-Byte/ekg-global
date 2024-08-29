import enum
from talib import abstract

from apps.stocks.models import Stock
from .criteria.functions import function_evaluator, Function


class SMAPrice(enum.Enum):
    OPEN = "open"
    CLOSE = "close"


@function_evaluator
def SMA(stock: Stock, function: Function):
    options = function.options
    kwds = {
        "timeperiod": int(options.get("timeperiod", 30)),
        "price": SMAPrice(options.get("price", "close")).value
    }
    close_list = stock.rates.values_list("close", flat=True)
    value = abstract.SMA(close_list, **kwds)
    return value
