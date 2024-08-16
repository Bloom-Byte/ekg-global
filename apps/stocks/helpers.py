from typing import Dict
import pandas as pd
from django.core.files import File
from dateutil.parser import parse

from .models import Rate, Stock, KSE100Rate


def get_trend(previous_close: float, close: float) -> str:
    """Get the market trend based on the previous close and current close."""
    if close > previous_close:
        return "up"
    elif close < previous_close:
        return "down"
    return "neutral"


UPDATEABLE_RATE_FIELDS = (
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

EXPECTED_RATE_COLUMNS = [
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

EXPECTED_KSE_COLUMNS = ["date", "open", "high", "low", "close", "volume"]


def handle_rates_file(rates_file: File) -> None:
    """
    Process the uploaded rates file.
    """
    df = pd.read_csv(rates_file, skip_blank_lines=True, keep_default_na=False)
    formatted_df = df[EXPECTED_RATE_COLUMNS]

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

    Rate.objects.bulk_create(new_rates, batch_size=998)
    Rate.objects.bulk_update(existing_rates, UPDATEABLE_RATE_FIELDS, batch_size=998)
    return None


def handle_kse_rates_file(kse_rates_file: File) -> None:
    """
    Process the uploaded KSE100 rates file.
    """
    df = pd.read_csv(kse_rates_file, skip_blank_lines=True, keep_default_na=False)
    formatted_df = df[EXPECTED_KSE_COLUMNS]

    kse_rates = []
    for row in formatted_df.itertuples():
        data: Dict = row._asdict()
        date = data.get("date", None)
        if date:
            data["date"] = parse(date).date()
        data.pop("Index")  # Remove the index from the data
        kse_rates.append(KSE100Rate(**data))

    KSE100Rate.objects.bulk_create(kse_rates, batch_size=998)
    return None
