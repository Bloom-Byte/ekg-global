import typing

from django.db import models

from .rate_providers import load_psx_rates, psx_rate_to_dict
from .data_cleaners import MGLinkStockRateDataCleaner
from apps.stocks.models import Stock, Rate, MarketType


def save_mg_link_psx_rates_data(mg_link_rates_data: typing.List[typing.Dict]):
    # Load first to ensure the data is valid and the
    # and the values are casted to their proper types
    stocks_rates = []

    for psx_rate in load_psx_rates(mg_link_rates_data):
        data = psx_rate_to_dict(psx_rate)
        stock_ticker = data["Symbol"]
        stock_title = data["CompanyName"]
        mg_link_company_id = data["CompanyId"]

        data_cleaner = MGLinkStockRateDataCleaner(rawdata=data)
        data_cleaner.clean()

        stock = Stock.objects.filter(
            models.Q(ticker__iexact=stock_ticker)
            | models.Q(metadata__mg_link_company_id=mg_link_company_id)
        ).first()
        if not stock:
            stock = Stock(
                ticker=stock_ticker, metadata={"mg_link_company_id": mg_link_company_id}
            )

        # Update the stock title here, just in case it is not set or it has changed
        stock.title = stock_title
        stock.save()

        stock_rate = data_cleaner.new_instance(stock=stock, market=MarketType.FUTURE)
        # Ensure that the rate does not already exist for the stock at the same time
        if Rate.objects.filter(stock=stock, added_at=stock_rate.added_at).exists():
            continue
        stocks_rates.append(stock_rate)

    return Rate.objects.bulk_create(stocks_rates)

