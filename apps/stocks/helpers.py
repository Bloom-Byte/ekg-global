from typing import Dict
import decimal
import pandas as pd
from django.core.files import File

from .models import Rate, Stock


def get_trend(previous_close: float, close: float) -> str:
    """Get the market trend based on the previous close and current close."""
    if close > previous_close:
        return "up"
    elif close < previous_close:
        return "down"
    return "neutral"


RATE_UPDATEABLE_FIELDS = (
    "market",
    "previous_close",
    "open",
    "high",
    "low",
    "close",
    "trend",
    "change",
    "volume",
)

EXPECTED_COLUMNS = [
    "ticker",
    "mkt",
    "previous_close",
    "open",
    "high",
    "low",
    "close",
    "change",
    "volume",
]


def handle_rates_file(rates_file: File) -> bool:
    """
    Process the uploaded rates file.

    :return:
    """
    df = pd.read_csv(rates_file)
    formatted_df = df[EXPECTED_COLUMNS]

    new_rates = []
    existing_rates = []
    for row in formatted_df.itertuples():
        data: Dict = row._asdict()
        data.pop("Index")  # Remove the index from the data
        data["trend"] = get_trend(data["previous_close"], data["close"])
        ticker = data.pop("ticker")
        data["market"] = data.pop("mkt")

        stock, created = Stock.objects.get_or_create(ticker=ticker)
        data["stock"] = stock
        if created:
            # If the stock is new, add the rate for creation
            new_rates.append(Rate(**data))
        else:
            # If the stock already exists, add the rate for update
            existing_rates.append(Rate(**data))

    Rate.objects.bulk_create(new_rates)
    Rate.objects.bulk_update(existing_rates, RATE_UPDATEABLE_FIELDS, batch_size=100)
    return True


def get_stock_latest_price(stock_ticker: str):
    stock = Stock.objects.get(ticker=stock_ticker)
    try:
        return stock.rate.close
    except Exception:
        return None
