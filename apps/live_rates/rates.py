import typing
import datetime

from helpers.logging import log_exception
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
        try:
            stock_ticker = data.get("symbol", None)
            if stock_ticker is None or not stock_ticker.strip():
                continue

            data_cleaner = MGLinkStockRateDataCleaner(data)
            data_cleaner.clean()

            stock_ticker = stock_ticker.strip()
            stock_created = False
            stock = Stock.objects.filter(ticker__iexact=stock_ticker).first()
            if not stock:
                stock_title = data.get("company_name", None)
                if stock_title:
                    stock_title = stock_title.strip()

                stock = Stock.objects.create(
                    ticker=stock_ticker.upper(),
                    title=stock_title,
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
        except Exception as exc:
            log_exception(exc)
            continue

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
