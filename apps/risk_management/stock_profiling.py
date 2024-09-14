import datetime
import decimal
import enum
import typing
from concurrent.futures import ThreadPoolExecutor

from apps.risk_management.models import RiskProfile
from apps.stocks.models import Stock
from apps.stocks.helpers import (
    get_kse_top30_stocks,
    get_kse_top50_stocks,
    get_kse_top100_stocks,
)
from helpers.utils.time import timeit
from helpers.utils.datetime import timedelta_code_to_datetime_range
from .criteria.criteria import Criteria, evaluate_criteria, CriterionStatus


def calculate_stock_percentage_return(
    stock: Stock, start_date: datetime.date, end_date: datetime.date
) -> decimal.Decimal:
    """
    Calculate the percentage return of a stock over a period of time.

    :param stock: A Stock object to calculate the return for
    :param start_date: The start date of the period
    :param end_date: The end date of the period
    :return: The percentage return of the stock
    """
    start_price = stock.get_price_on_date(start_date)
    end_price = stock.get_price_on_date(end_date)

    if not start_price or not end_price:
        return decimal.Decimal(0).quantize(
            decimal.Decimal(0.01), rounding=decimal.ROUND_HALF_UP
        )
    return (((end_price - start_price) / start_price) * 100).quantize(
        decimal.Decimal(0.01), rounding=decimal.ROUND_HALF_UP
    )


def calculate_percentage_ranking(evaluation_result: typing.Dict[str, CriterionStatus]) -> int:
    """Calculate the percentage ranking of the stock based on the evaluation result."""
    score = sum((status.value for status in evaluation_result.values()))
    expected_score = sum((CriterionStatus.PASSED.value for _ in evaluation_result))
    return round((score / expected_score) * 100)


PERCENTAGE_RETURN_INDICATORS_TIMEDELTA_CODES = (
    "1D",
    "3D",
    "1W",
    "1M",
    "YTD",
)


def generate_stock_profile(stock: Stock, criteria: Criteria) -> dict:
    """
    Generates the risk profile for a single stock.

    :param stock: A Stock object to evaluate
    :param criteria: The criteria to evaluate the stock against
    :return: A dictionary containing the stock's profile and evaluation
    """
    stock_profile = {}
    # First add the basic information about the stock
    stock_profile["symbol"] = stock.ticker
    stock_profile["close"] = stock.price

    # Calculate the percentage return for the stock over different time periods
    # Update the stock profile with the percentage return for each time period
    for timedelta_code in PERCENTAGE_RETURN_INDICATORS_TIMEDELTA_CODES:
        start, end = timedelta_code_to_datetime_range(timedelta_code)
        percentage_return = calculate_stock_percentage_return(
            stock, start.date(), end.date()
        )
        stock_profile[f"{timedelta_code} return (%)"] = float(percentage_return)

    evaluation_result = evaluate_criteria(stock, criteria=criteria)
    percentage_ranking = calculate_percentage_ranking(evaluation_result)
    stock_profile.update(evaluation_result)
    # This is the percentage ranking of the stock based on the evaluation result
    # It should be the last key in the dictionary
    stock_profile["EK score (%)"] = percentage_ranking
    return stock_profile


@timeit
def generate_stocks_risk_profile(
    stocks: typing.Union[
        typing.Iterable[Stock], typing.Callable[[], typing.Iterable[Stock]]
    ],
    *,
    criteria: Criteria,
) -> list:
    """
    Generate the risk profile for the given stocks in parallel using ThreadPoolExecutor and map.

    :param stocks: A list of stocks or a callable that returns a list of stocks
    :param criteria: The criteria to evaluate the stocks against
    :return: A list of results of each stock's evaluation
    """
    if callable(stocks):
        stocks = stocks()
    if not stocks:
        return []

    with ThreadPoolExecutor() as executor:
        profiles = list(
            executor.map(lambda stock: generate_stock_profile(stock, criteria), stocks)
        )

    return profiles


class StockSet(enum.Enum):
    KSE100 = "kse100"
    KSE50 = "kse50"
    KSE30 = "kse30"
    CUSTOM = "custom"


StockSetResolver = typing.Callable[
    [RiskProfile],
    typing.Union[typing.Iterable[Stock], typing.Callable[[], typing.Iterable[Stock]]],
]
STOCKSET_RESOLVERS: typing.Dict[StockSet, StockSetResolver] = {}


def stockset_resolver(stockset: StockSet):
    stockset = StockSet(stockset)

    def decorator(resolver):
        global STOCKSET_RESOLVERS
        STOCKSET_RESOLVERS[stockset] = resolver
        return resolver

    return decorator


def resolve_stockset(stockset: typing.Union[str, StockSet], risk_profile: RiskProfile):
    stockset = StockSet(stockset)
    try:
        resolver = STOCKSET_RESOLVERS[stockset]
    except KeyError:
        return []
    return resolver(risk_profile)


@stockset_resolver(StockSet.KSE100)
def _(_):
    return get_kse_top100_stocks()


@stockset_resolver(StockSet.KSE50)
def _(_):
    return get_kse_top50_stocks()


@stockset_resolver(StockSet.KSE30)
def _(_):
    return get_kse_top30_stocks()


@stockset_resolver(StockSet.CUSTOM)
def _(risk_profile: RiskProfile):
    return risk_profile.stocks.all()
