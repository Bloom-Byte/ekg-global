import typing
import functools
from concurrent.futures import ThreadPoolExecutor

from apps.stocks.models import Stock
from apps.stocks.helpers import (
    get_kse_top30_stocks,
    get_kse_top50_stocks,
    get_kse_top100_stocks,
)
from helpers.utils.time import timeit
from .criteria.criteria import Criteria, evaluate_criteria


@timeit
def generate_stocks_risk_profile(
    stocks: typing.Union[
        typing.Iterable[Stock], typing.Callable[[], typing.Iterable[Stock]]
    ],
    *,
    criteria: Criteria,
):
    """
    Generate the risk profile for the given stocks

    :param stocks: A list of stocks or a callable that returns a list of stocks
    :param criteria: The criteria to evaluate the stocks against
    :return: A list of results of each stock's evaluation
    """
    if callable(stocks):
        stocks = stocks()
    if not stocks:
        return []
    
    results = []
    for stock in stocks:
        result = evaluate_criteria(stock, criteria=criteria)
        result["Stock"] = stock.ticker
        results.append(result)
    return list(results)


generate_kse30_risk_profile = functools.partial(
    generate_stocks_risk_profile, stocks=get_kse_top30_stocks
)
generate_kse50_risk_profile = functools.partial(
    generate_stocks_risk_profile, stocks=get_kse_top50_stocks
)
generate_kse100_risk_profile = functools.partial(
    generate_stocks_risk_profile, stocks=get_kse_top100_stocks
)
