import typing
import datetime
from django.db import models

from helpers.utils.time import timeit

from .rate_providers import cleaned_rates_data, mg_link_provider
from .data_cleaners import MGLinkStockRateDataCleaner
from apps.stocks.models import Stock, Rate, MarketType


@timeit
def save_mg_link_psx_rates_data(mg_link_rates_data: typing.List[typing.Dict]):
    # Load first to ensure the data is valid and the
    # and the values are casted to their proper types
    stocks_rates = []

    for data in cleaned_rates_data(mg_link_rates_data):
        stock_ticker = data["symbol"]
        stock_title = data["company_name"]
        mg_link_company_id = data["company_id"]

        data_cleaner = MGLinkStockRateDataCleaner(data)
        data_cleaner.clean()

        stock_created = False
        stock = Stock.objects.filter(
            models.Q(ticker__iexact=stock_ticker)
            | models.Q(metadata__mg_link_company_id__iexact=str(mg_link_company_id))
        ).first()
        if not stock:
            stock = Stock.objects.create(
                ticker=stock_ticker,
                title=stock_title,
                metadata={"mg_link_company_id": str(mg_link_company_id)},
            )
            stock_created = True

        stock_rate = data_cleaner.new_instance(stock=stock, market=MarketType.FUTURE)
        # If the rate already exist for the stock and the added_at date
        # Ignore the rate and continue to the next one
        if (
            not stock_created
            and Rate.objects.filter(
                stock_id=stock.id, added_at=stock_rate.added_at
            ).exists()
        ):
            continue
        stocks_rates.append(stock_rate)

    return Rate.objects.bulk_create(stocks_rates, batch_size=5000)


def update_stock_rates(
    start_date: typing.Optional[datetime.date] = None,
    end_date: typing.Optional[datetime.date] = None,
):
    """
    Update stock rates data in DB with  rates from MGLink.

    :param start_date: Start date to fetch rates from.
    :param end_date: End date to fetch rates from.
    """
    rates_data = mg_link_provider.fetch_psx_rates(start_date, end_date)
    save_mg_link_psx_rates_data(rates_data)
