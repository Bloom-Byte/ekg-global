import typing
import functools
from concurrent.futures import ThreadPoolExecutor

from apps.stocks.models import Stock
from apps.stocks.helpers import (
    get_kse_top30_stocks,
    get_kse_top50_stocks,
    get_kse_top100_stocks,
)
from .criteria.criteria import Criteria, evaluate_criteria
from helpers.caching import ttl_cache


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

    # Just in case we have repeated stocks, 
    # This will make sure to only evaluate each stock once
    _evaluate_criteria = ttl_cache(ttl=60)(evaluate_criteria)
    with ThreadPoolExecutor() as executor:
        results = executor.map(
            lambda stock: _evaluate_criteria(stock, criteria=criteria),
            stocks,
        )
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
