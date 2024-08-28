import csv
import typing
import pandas as pd
import io
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction

from apps.portfolios.models import Investment, Portfolio
from apps.stocks.models import Stock
from apps.accounts.models import UserAccount
from .data_cleaners import InvestmentDataCleaner
from helpers.utils.misc import comma_separated_to_int_float

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
    NUMBER_COLUMNS = (
        "BUY",
        "SELL",
        "RATE",
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
    )
    converters = {column: comma_separated_to_int_float for column in NUMBER_COLUMNS}
    df = pd.read_csv(
        transactions_file,
        skip_blank_lines=True,
        keep_default_na=False,
        converters=converters,
    )

    # Ensure all expected columns are present in the DataFrame
    missing_columns = set(EXPECTED_TRANSACTION_COLUMNS) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing columns in transactions file: {missing_columns}")

    new_investments = []
    for row in df.itertuples(index=False):
        data: typing.Dict = {
            col: getattr(row, col) for col in EXPECTED_TRANSACTION_COLUMNS
        }

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
        ) * investment.base_cost
        new_investments.append(investment)

    Investment.objects.bulk_create(new_investments, batch_size=998)
    return None


def get_transactions_upload_template() -> InMemoryUploadedFile:
    """
    Generate an upload template for transactions, with the correct columns.
    """
    str_io = io.StringIO()
    writer = csv.writer(str_io)
    writer.writerow(
        EXPECTED_TRANSACTION_COLUMNS
    )  # Write the expected columns as the header
    str_io.seek(0)

    in_memory_file = InMemoryUploadedFile(
        file=str_io,
        field_name=None,
        name="transactions.csv",
        content_type="application/csv",
        size=len(str_io.getvalue().encode()),
        charset=None,
    )
    return in_memory_file
