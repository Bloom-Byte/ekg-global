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
from .criteria.criteria import Criteria, evaluate_criteria, CriterionStatus


def calculate_percentage_ranking(evaluation_result: typing.Dict[str, CriterionStatus]):
    score = sum((status.value for status in evaluation_result.values()))
    expected_score = sum((CriterionStatus.PASSED.value for _ in evaluation_result))
    return round((score / expected_score) * 100)


def generate_stock_profile(stock: Stock, criteria: Criteria) -> dict:
    """
    Generates the risk profile for a single stock.

    :param stock: A Stock object to evaluate
    :param criteria: The criteria to evaluate the stock against
    :return: A dictionary containing the stock's profile and evaluation
    """
    profile = {}
    profile["stock"] = stock.ticker
    profile["current rate"] = stock.price

    evaluation_result = evaluate_criteria(stock, criteria=criteria)
    percentage_ranking = calculate_percentage_ranking(evaluation_result)
    profile.update(evaluation_result)
    profile["ranking"] = percentage_ranking

    return profile


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
