from concurrent.futures import ThreadPoolExecutor
import datetime
import decimal
import csv
import functools
import io
import typing
import asyncio
import pandas as pd
from django.db import models, transaction
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile

try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo

from .models import Investment, Portfolio
from apps.stocks.models import KSE100Rate, Stock
from apps.accounts.models import UserAccount
from helpers.utils.colors import random_colors
from helpers.utils.models import get_objects_within_datetime_range
from helpers.utils.datetime import split
from helpers.caching import ttl_cache
from .data_cleaners import InvestmentDataCleaner
from helpers.utils.time import timeit
from helpers.models.db import database_sync_to_async
from helpers.utils.misc import merge_dicts


def get_portfolio_allocation_data(portfolio: Portfolio) -> typing.Dict[str, float]:
    """
    Returns a mapping of the ticker symbols of stocks invested in,
    to the respective principal amounts invested in them, in a portfolio
    """
    allocation_data = {}

    for investment in portfolio.investments.select_related("stock").all():
        allocation_data[investment.symbol] = allocation_data.get(
            investment.symbol, 0.00
        ) + float(abs(investment.principal))
    return allocation_data


def get_portfolio_allocation_piechart_data(portfolio: Portfolio) -> str:
    """Returns the portfolio's stock allocation data in a format suitable for Chart.js pie chart."""
    allocation_data = get_portfolio_allocation_data(portfolio)
    colors = [next(random_colors()) for _ in range(len(allocation_data))]
    return {"data": allocation_data, "colors": colors}


# The investments based function for fetching allocation
# data is slightly efficient than the portfolio based function
def get_investments_allocation_data(
    investments: models.QuerySet[Investment],
) -> typing.Dict[str, float]:
    """
    Returns a mapping of the ticker symbols of stocks invested in,
    to the respective principal amounts invested in them, from the investments given.
    """
    allocation_data = {}

    for investment in investments:
        allocation_data[investment.symbol] = allocation_data.get(
            investment.symbol, 0.00
        ) + float(abs(investment.principal))
    return allocation_data


def get_investments_allocation_piechart_data(
    investments: models.QuerySet[Investment],
) -> str:
    """Returns the investments' stock allocation data in a format suitable for Chart.js pie chart."""
    allocation_data = get_investments_allocation_data(investments)
    colors = [next(random_colors()) for _ in range(len(allocation_data))]
    return {"data": allocation_data, "colors": colors}


def get_close_price_range_for_period(
    rate_model_or_qs: typing.Union[models.Model, models.QuerySet],
    /,
    period_start: typing.Union[datetime.date, datetime.datetime],
    period_end: typing.Union[datetime.date, datetime.datetime],
    dt_field: str,
):
    """
    Returns the minimum and maximum close prices within a specified date/datetime period

    :param rate_model_or_qs: rate model or queryset to filter on.
    :param period_start: start date/datetime of the period.
    :param period_end: end date/datetime of the period.
    :param dt_field: The date/datetime field to filter on.
    :return: The minimum and maximum close prices within the specified period.
    """
    rates = get_objects_within_datetime_range(
        rate_model_or_qs, period_start, period_end, dt_field
    )
    aggregate = rates.aggregate(
        min_close=models.Min("close"), max_close=models.Max("close")
    )
    min_close = aggregate.get("min_close")
    max_close = aggregate.get("max_close")
    return min_close, max_close


DT_FILTERS_TO_DAY_DELTA = {
    "5D": 5,
    "1W": 7,
    "1M": 30,
    "3M": 90,
    "6M": 180,
    "1Y": 365,
    "5Y": 365 * 5,
    "YTD": 0,
}


@ttl_cache
def parse_dt_filter(
    dt_filter: str, timezone: str = None
) -> typing.Tuple[typing.Optional[datetime.date], datetime.date]:
    """
    Parses the datetime filter into a start and end date,
    based on the correspoding values defined in DT_FILTERS_TO_DAY_DELTA.

    :param dt_filter: The datetime filter to parse.
    :param timezone: The preferred timezone to use.
    :return: A tuple containing the start and end date.
    :raises ValueError: If the filter is invalid.
    """
    day_delta = DT_FILTERS_TO_DAY_DELTA.get(dt_filter, None)
    if day_delta is None:
        raise ValueError(f"Invalid datetime filter: {dt_filter}")

    delta = datetime.timedelta(days=float(day_delta))
    tz = zoneinfo.ZoneInfo(timezone) if timezone else None
    todays_date = datetime.datetime.now(tz).date()

    end_date = todays_date
    if not day_delta:
        start_date = None
    else:
        start_date = todays_date - delta
    return start_date, end_date


@timeit
@ttl_cache(ttl=60 * 5)
def get_kse_performance_data(
    dt_filter: str, timezone: typing.Optional[str] = None
) -> typing.Dict[str, float]:
    """
    Returns the KSE100 performance data for the time period
    specified by the datetime filter.

    :param dt_filter: The datetime filter to use.
    :param timezone: The preferred timezone to use.
    """
    start_date, end_date = parse_dt_filter(dt_filter, timezone)
    if not start_date:
        # If the start date is None, use the date of the first KSE100Rate
        earliest_rate = KSE100Rate.objects.order_by("date").first()
        if earliest_rate:
            start_date = earliest_rate.date

    delta = None

    def get_kse_performance_data_for_period(period_start, period_end):
        nonlocal kse_performance_data, delta
        if delta is None:
            delta = period_end - period_start

        pre_period_start = period_start - delta

        pre_period_start_price = KSE100Rate.get_close_on_date(pre_period_start)
        period_start_price = KSE100Rate.get_close_on_date(period_start)
        period_end_price = KSE100Rate.get_close_on_date(period_end)

        percentage_change_at_period_start = 0.00
        percentage_change_at_period_end = 0.00
        if pre_period_start_price and period_start_price:
            percentage_change_at_period_start = (
                (period_start_price - pre_period_start_price) / pre_period_start_price
            ) * 100

        if period_start_price and period_end_price:
            percentage_change_at_period_end = (
                (period_end_price - period_start_price) / period_start_price
            ) * 100

        return {
            period_start.isoformat(): percentage_change_at_period_start,
            period_end.isoformat(): percentage_change_at_period_end,
        }

    async def main():
        async_func = database_sync_to_async(get_kse_performance_data_for_period)
        tasks = []
        for periods in split(start_date, end_date, parts=5):
            task = asyncio.create_task(async_func(*periods))
            tasks.append(task)

        return await asyncio.gather(*tasks)

    results = asyncio.run(main())
    # Merge the results such that the most recent result updates the existing one
    kse_performance_data = functools.reduce(merge_dicts, results)
    return kse_performance_data


def get_portfolio_percentage_return_on_dates(
    portfolio: Portfolio, *dates: datetime.date
):
    if not dates:
        raise ValueError()

    with ThreadPoolExecutor() as executor:
        result = executor.map(portfolio.get_percentage_return_on_investments, dates)
    return list(result)


@ttl_cache
def get_investment_percentage_return_on_dates(
    investment: Investment, *dates: datetime.date
):
    if not dates:
        raise ValueError()

    with ThreadPoolExecutor() as executor:
        result = executor.map(
            lambda date: investment.get_percentage_return_on_date(date)
            or decimal.Decimal(0),
            dates,
        )
    return list(result)


@timeit
def get_portfolio_performance_data(
    portfolio: Portfolio,
    dt_filter: str,
    timezone: str = None,
    stocks: typing.Optional[typing.List[str]] = None,
) -> typing.Dict[str, typing.Dict[str, float]]:
    portfolio_investments = portfolio.investments.select_related("stock")
    start_date, end_date = parse_dt_filter(dt_filter, timezone)
    if not start_date:
        # If the start date is None, use the date the portfolio was created
        start_date = portfolio.created_at.date()

    def get_portfolio_percentage_return_values_for_period(period_start, period_end):
        nonlocal percentage_return_values
        percentage_returns = get_portfolio_percentage_return_on_dates(
            portfolio, period_start, period_end
        )
        return {
            period_start.isoformat(): float(percentage_returns[0]),
            period_end.isoformat(): float(percentage_returns[1]),
        }

    def get_investment_percentage_return_values_for_period(period_start, period_end):
        nonlocal percentage_return_values
        nonlocal stocks
        period_start_iso_fmt = period_start.isoformat()
        period_end_iso_fmt = period_end.isoformat()
        result = {}

        for stock in stocks:
            investment: Investment = portfolio_investments.filter(
                stock__ticker=stock
            ).first()
            if not investment:
                continue
            percentage_returns = get_investment_percentage_return_on_dates(
                investment, period_start, period_end
            )
            result[stock] = {
                period_start_iso_fmt: float(percentage_returns[0]),
                period_end_iso_fmt: float(percentage_returns[1]),
            }
        return result

    if stocks:
        func = get_investment_percentage_return_values_for_period
    else:
        func = get_portfolio_percentage_return_values_for_period

    async def main():
        async_func = database_sync_to_async(func)
        tasks = []
        for periods in split(start_date, end_date, parts=5):
            task = asyncio.create_task(async_func(*periods))
            tasks.append(task)

        return await asyncio.gather(*tasks)

    results = asyncio.run(main())
    # Merge the results such that the most recent result updates the existing one
    percentage_return_values = functools.reduce(merge_dicts, results)
    if stocks:
        return percentage_return_values
    return {"all": percentage_return_values}


@timeit
def get_portfolio_performance_graph_data(
    portfolio: Portfolio,
    dt_filter: str = "5D",
    timezone: str = None,
    stocks: typing.Optional[typing.List[str]] = None,
) -> typing.Dict[str, float]:
    """
    Returns an aggregates the portfolio investments and
    KSE100 performance data to be plotted on a line graph

    :param portfolio: The portfolio to get performance data for.
    :param dt_filter: The datetime filter to use.
    :param timezone: The preferred timezone to use.
    :param stocks: Limit performance data aggregation to include
        only investments in these stocks(stocks with the ticker symbol).
    """
    try:
        kse_performance_data = get_kse_performance_data(dt_filter, timezone)
    except ValueError:
        kse_performance_data = {}
    try:
        portfolio_performance_data = get_portfolio_performance_data(
            portfolio=portfolio, dt_filter=dt_filter, timezone=timezone, stocks=stocks
        )
    except ValueError:
        portfolio_performance_data = {}

    colors = {}
    colors["KSE100"] = next(random_colors())
    for key in portfolio_performance_data:
        colors[key] = next(random_colors())

    return {
        "KSE100": kse_performance_data,
        "portfolio": portfolio_performance_data,
        "colors": colors,
    }


def get_stocks_invested_from_portfolio(portfolio: Portfolio) -> typing.List[str]:
    stock_tickers = portfolio.investments.select_related("stock").values_list(
        "stock__ticker", flat=True
    )
    return list(set(stock_tickers))


def get_stocks_invested_from_investments(
    investments: models.QuerySet[Investment],
) -> typing.List[str]:
    stock_tickers = investments.values_list("stock__ticker", flat=True)
    return list(set(stock_tickers))


EXPECTED_TRANSACTION_COLUMNS = [
    "TRDATE",
    "STDATE",
    "TIME",
    "LOC",
    "DEALER",
    "CLIENT",
    "OCCUPATION",
    "RESIDENCE",
    "UIN",
    "CLIENT_CAT",
    "CDCID",
    "CLIENT_TITLE",
    "SYMBOL",
    "SYMBOL_TITLE",
    "BUY",
    "SELL",
    "RATE",
    "FLAG",
    "BOOK",
    "TR_TYPE",
    "COT_ST",
    "KORDER",
    "TICKET",
    "TERMINAL",
    "BILL",
    "COMM",
    "CDC",
    "CVT",
    "WHTS",
    "WHTC",
    "LAGA",
    "SECP",
    "NLAGA",
    "FED",
    "MISC",
]


@transaction.atomic
def handle_transactions_file(transactions_file: File, user: UserAccount) -> None:
    """
    Process the uploaded transactions file.
    """
    df = pd.read_csv(transactions_file, skip_blank_lines=True, keep_default_na=False)
    formatted_df = df[EXPECTED_TRANSACTION_COLUMNS]

    new_investments = []
    for row in formatted_df.itertuples():
        data: typing.Dict = row._asdict()
        # print(data)
        data.pop("Index")  # Remove the index from the data
        unique_id = data["UIN"]
        stock_ticker = data["SYMBOL"]
        stock_title = data["SYMBOL_TITLE"]
        buy_quantity = data["BUY"]
        sell_quantity = data["SELL"]

        if buy_quantity and sell_quantity:
            raise ValueError(
                "A transaction can either be 'BUY' or 'SELL' type, not both."
            )
        if not (buy_quantity or sell_quantity):
            raise ValueError("Either 'BUY' or 'SELL' quantity must be provided.")

        transaction_type = "buy" if buy_quantity else "sell"
        quantity = int(buy_quantity) if buy_quantity else int(sell_quantity)
        data_cleaner = InvestmentDataCleaner(data)
        data_cleaner.clean()

        # Get or create the stock with the symbol/ticker
        stock, created = Stock.objects.get_or_create(ticker=stock_ticker)
        if created or not stock.title:
            stock.title = stock_title
            stock.save()

        # Create portfolio with unique ID
        portfolio, _ = Portfolio.objects.get_or_create(name=unique_id, owner=user)
        investment = data_cleaner.new_instance(
            portfolio=portfolio,
            stock=stock,
            quantity=quantity,
            transaction_type=transaction_type,
        )
        investment.brokerage_fee = (
            portfolio.brokerage_percentage / 100
        ) * investment.base_principal
        new_investments.append(investment)

    Investment.objects.bulk_create(new_investments, batch_size=998)
    return None


def get_transactions_upload_template() -> InMemoryUploadedFile:
    str_io = io.StringIO()
    str_io.seek(0)

    writer = csv.writer(str_io)
    writer.writerow(EXPECTED_TRANSACTION_COLUMNS)

    in_memory_file = InMemoryUploadedFile(
        file=str_io,
        field_name=None,
        name="transactions.csv",
        content_type="application/csv",
        size=len(str_io.getvalue().encode()),
        charset=None,
    )
    return in_memory_file
