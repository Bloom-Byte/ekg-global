import typing
import functools

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
    
    profiles = []
    for stock in stocks:
        profile = {}
        profile["stock"] = stock.ticker
        profile["current rate"] = stock.price

        evaluation_result = evaluate_criteria(stock, criteria=criteria)
        percentage_ranking = calculate_percentage_ranking(evaluation_result)
        profile.update(evaluation_result)
        profile["ranking"] = percentage_ranking

        profiles.append(profile)
    return list(profiles)


generate_kse30_risk_profile = functools.partial(
    generate_stocks_risk_profile, stocks=get_kse_top30_stocks
)
generate_kse50_risk_profile = functools.partial(
    generate_stocks_risk_profile, stocks=get_kse_top50_stocks
)
generate_kse100_risk_profile = functools.partial(
    generate_stocks_risk_profile, stocks=get_kse_top100_stocks
)
