import typing
import functools
import attrs
import decimal
from concurrent.futures import ThreadPoolExecutor
from django.db import models

from apps.portfolios.helpers import get_stocks_invested_from_investments
from apps.portfolios.models import Portfolio, Investment
from apps.portfolios.profiling import (
    get_stock_profile_from_investments,
    convert_to_2dp_decimal,
)


@attrs.define(auto_attribs=True, kw_only=True)
class StockRiskProfile:
    average_cost: typing.Optional[decimal.Decimal] = attrs.field(
        default=None, converter=convert_to_2dp_decimal
    )
    current_rate: typing.Optional[decimal.Decimal] = attrs.field(
        default=None, converter=convert_to_2dp_decimal
    )


RiskProfile = typing.List[StockRiskProfile]


def generate_stock_risk_profile_from_investments(
    stock: str, investments: models.QuerySet[Investment]
):
    stock_profile = get_stock_profile_from_investments(stock, investments)
    average_cost = stock_profile.net_average_cost
    current_rate = stock_profile.market_rate
    return StockRiskProfile(
        **{"average_cost": average_cost, "current_rate": current_rate}
    )


def generate_risk_profile(
    portfolio: Portfolio,
    *,
    stocks: typing.Optional[
        typing.Union[typing.Iterable[str], typing.Callable[..., typing.Iterable[str]]]
    ] = None,
) -> RiskProfile:
    """
    Generate a risk profile for a portfolio.

    :param portfolio: Portfolio instance
    :param stocks: stocks in the portfolio to generate a risk profile for
    :return: A list containing the risk profile of all/selected stocks in the portfolio
    """
    portfolio_investments = (
        portfolio.investments.select_related("stock")
        .prefetch_related("stock__rates")
        .all()
    )

    target_stocks = (
        stocks
        if stocks is not None
        else get_stocks_invested_from_investments(portfolio_investments)
    )
    if callable(target_stocks):
        target_stocks = target_stocks()
    if not target_stocks:
        return []

    with ThreadPoolExecutor() as executor:
        results = executor.map(
            lambda stock: generate_stock_risk_profile_from_investments(
                stock, portfolio_investments
            ),
            set(target_stocks),
        )
    return list(results)


def get_kse_top30_stocks(): ...
def get_kse_top50_stocks(): ...
def get_kse_top100_stocks(): ...


generate_kse30_risk_profile = functools.partial(
    generate_risk_profile, stocks=get_kse_top30_stocks
)
generate_kse50_risk_profile = functools.partial(
    generate_risk_profile, stocks=get_kse_top50_stocks
)
generate_kse100_risk_profile = functools.partial(
    generate_risk_profile, stocks=get_kse_top100_stocks
)
