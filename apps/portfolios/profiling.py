import typing
import decimal
import functools
import attrs
from concurrent.futures import ThreadPoolExecutor
from django.db import models

from .helpers import parse_dt_filter, get_stocks_invested_from_investments
from .models import TransactionType, Portfolio, Investment
from apps.stocks.models import Rate
from helpers.utils.time import timeit
from helpers.utils.decimals import to_n_decimal_places


convert_to_2dp_decimal = functools.partial(to_n_decimal_places, n=2)


@attrs.define(auto_attribs=True, kw_only=True)
class StockProfile:
    """Model to represent a stock's profile in a portfolio"""

    symbol: str
    net_quantity: int = 0
    average_rate: typing.Optional[decimal.Decimal] = attrs.field(
        default=None, converter=convert_to_2dp_decimal
    )
    net_average_cost: typing.Optional[decimal.Decimal] = attrs.field(
        default=None, converter=convert_to_2dp_decimal
    )
    market_rate: typing.Optional[decimal.Decimal] = attrs.field(
        default=None, converter=convert_to_2dp_decimal
    )
    market_value: typing.Optional[decimal.Decimal] = attrs.field(
        default=None, converter=convert_to_2dp_decimal
    )
    net_return_on_investments: typing.Optional[decimal.Decimal] = attrs.field(
        default=None, converter=convert_to_2dp_decimal
    )
    percentage_return_on_investments: typing.Optional[decimal.Decimal] = attrs.field(
        default=None, converter=convert_to_2dp_decimal
    )
    percentage_allocation: typing.Optional[decimal.Decimal] = attrs.field(
        default=None, converter=convert_to_2dp_decimal
    )


def get_stock_profile_from_investments(
    stock: str, investments: models.QuerySet[Investment]
) -> StockProfile:
    investments_for_stock = investments.filter(stock__ticker=stock)
    # If no investments exists, return a stock profile with the default attributes
    if not investments_for_stock.exists():
        return StockProfile(symbol=stock)

    annotated_qs = investments_for_stock.annotate(
        signed_quantity=models.Case(
            models.When(
                transaction_type=TransactionType.SELL, then=-models.F("quantity")
            ),
            default=models.F("quantity"),
            output_field=models.IntegerField(),
        )
    )
    aggregation = annotated_qs.aggregate(
        net_quantity=models.Sum("signed_quantity"),
        average_rate=models.Avg("rate"),
    )

    net_quantity: int = aggregation["net_quantity"]
    average_rate = aggregation["average_rate"]
    net_average_cost = float(net_quantity * average_rate)
    latest_rate_record = (
        Rate.objects.filter(stock__ticker=stock).order_by("-added_at").first()
    )

    market_rate = None
    market_value = None
    net_return_on_investments = None
    percentage_return_on_investments = None
    if latest_rate_record:
        # Get the current/latest (market) rate
        market_rate = latest_rate_record.close

    if market_rate and net_average_cost:
        market_value = abs(net_quantity) * market_rate
        net_return_on_investments = market_value - net_average_cost
        percentage_return_on_investments = (
            net_return_on_investments / abs(net_average_cost)
        ) * 100

    return StockProfile(
        **{
            "symbol": stock,
            "net_quantity": net_quantity,
            "average_rate": average_rate,
            "net_average_cost": net_average_cost,
            "market_rate": market_rate,
            "market_value": market_value,
            "net_return_on_investments": net_return_on_investments,
            "percentage_return_on_investments": percentage_return_on_investments,
        }
    )


def _update_stock_profile_with_percentage_allocation(
    stock_profile: StockProfile,
    total_quantity_of_stocks_invested_in: int,
):
    if not total_quantity_of_stocks_invested_in:
        stock_profile.percentage_allocation = None
        return stock_profile

    net_quantity = stock_profile.net_quantity
    percentage_allocation = (net_quantity / total_quantity_of_stocks_invested_in) * 100
    stock_profile.percentage_allocation = percentage_allocation
    return stock_profile


@timeit
def generate_portfolio_stock_profiles(
    portfolio: Portfolio, dt_filter: str = "5D", timezone: str = None
) -> typing.List[StockProfile]:
    start_date, _ = parse_dt_filter(dt_filter, timezone)
    portfolio_investments = (
        portfolio.investments.select_related("stock")
        .prefetch_related("stock__rates")
        .filter(added_at__date__gte=start_date)
    )

    # If no investments exists, return a profile for the total only
    if not portfolio_investments.exists():
        return [StockProfile(symbol="TOTAL")]

    stocks_invested_in = get_stocks_invested_from_investments(portfolio_investments)
    with ThreadPoolExecutor() as executor:
        stock_profiles = list(
            executor.map(
                lambda stock: get_stock_profile_from_investments(
                    stock, portfolio_investments
                ),
                stocks_invested_in,
            )
        )

    net_total_quantity_of_stocks_invested_in = sum(
        profile.net_quantity for profile in stock_profiles
    )
    net_total_average_cost = sum(profile.net_quantity for profile in stock_profiles)
    total_market_value = sum(
        profile.market_value for profile in stock_profiles if profile.market_value
    )
    net_total_return_on_investments = sum(
        profile.net_return_on_investments
        for profile in stock_profiles
        if profile.net_return_on_investments
    )

    for profile in stock_profiles:
        profile = _update_stock_profile_with_percentage_allocation(
            profile, net_total_quantity_of_stocks_invested_in
        )

    total_profile = StockProfile(
        **{
            "symbol": "TOTAL",
            "net_quantity": net_total_quantity_of_stocks_invested_in,
            "average_rate": None,
            "net_average_cost": net_total_average_cost,
            "market_rate": None,
            "market_value": total_market_value,
            "net_return_on_investments": net_total_return_on_investments,
            "percentage_return_on_investments": None,
            "percentage_allocation": 100.00
            if net_total_quantity_of_stocks_invested_in
            else None,
        }
    )
    stock_profiles.append(total_profile)
    return stock_profiles
