import functools
import decimal
import uuid
import math
import datetime
import typing
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError



class Portfolio(models.Model):
    """Model definition for Portfolio."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        "accounts.UserAccount",
        on_delete=models.CASCADE,
        related_name="portfolios",
        db_index=True,
    )
    name = models.CharField(max_length=150)
    capital = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    description = models.TextField(null=True, blank=True)
    brokerage_percentage = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True, default=decimal.Decimal(15.00)
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Portfolio")
        verbose_name_plural = _("Portfolios")
        ordering = ["-created_at"]
        unique_together = [
            "owner",
            "name",
        ]  # user can have only one portfolio with a given name

    def __str__(self) -> str:
        return self.name

    @property
    def cash_balance(self) -> decimal.Decimal:
        """The remaining cash balance in the portfolio."""
        return (self.capital - self.invested_capital).quantize(
            decimal.Decimal("0.01"), rounding=decimal.ROUND_HALF_UP
        )
    
    @property
    def value(self) -> decimal.Decimal:
        """
        The current value of the portfolio.
        
        The sum of the value of investments in the portfolio,
        and the remaining cash balance. Or, the initial capital
        plus the total return on investments.
        """
        return self.get_value()

    @property
    def invested_capital(self):
        """
        The total capital invested in the portfolio.

        the total capital used as investment principal
        """
        total_investments_principal = math.fsum(self.investments_principals())
        return decimal.Decimal.from_float(total_investments_principal).quantize(
            decimal.Decimal("0.01"), rounding=decimal.ROUND_HALF_UP
        )
    
    @property
    def total_return_on_investments(self):
        """
        The total return on all investments in the portfolio.

        The current return on the invested capital.
        """
        return self.get_total_return_on_investments()
    
    @property
    def percentage_return_on_investments(self):
        """The current percentage return on the invested capital."""
        return self.get_percentage_return_on_investments()
    
    @property
    def total_investments_value(self):
        """
        The total of the current value of all investments in the portfolio.
        
        The current value of invested capital.
        """
        return self.get_total_investments_value()
    
    def investments_principals(self):
        """Yields the capital invested (principal) in each investment in the portfolio."""
        for investment in self.investments.all():
            yield investment.principal

    def investments_values(self, date: typing.Optional[datetime.date] = None):
        """
        Yields the current value of each investment in the portfolio.

        :
        """
        for investment in self.investments.all():
            if date:
                value = investment.get_value_on_date(date)
            else:
                value = investment.value
            if not value:
                continue
            yield value

    def returns_on_investments(self, date: typing.Optional[datetime.date] = None):
        """
        Yields the return on each investment in the portfolio.

        :param 
        """
        for investment in self.investments.all():
            if date:
                return_value = investment.get_return_value_on_date(date)
            else:
                return_value = investment.return_value
            if not return_value:
                continue
            yield return_value

    def get_total_investments_value(self, date: typing.Optional[datetime.date] = None):
        total_investments_value = math.fsum(self.investments_values(date))
        return decimal.Decimal.from_float(total_investments_value).quantize(
            decimal.Decimal("0.01"), rounding=decimal.ROUND_HALF_UP
        )

    def get_total_return_on_investments(self, date: typing.Optional[datetime.date] = None):
        total_return_on_investments = math.fsum(self.returns_on_investments(date))
        return decimal.Decimal.from_float(total_return_on_investments).quantize(
            decimal.Decimal("0.01"), rounding=decimal.ROUND_HALF_UP
        )
    
    def get_percentage_return_on_investments(self, date: typing.Optional[datetime.date] = None):
        invested_capital = self.invested_capital
        if invested_capital == 0:
            return decimal.Decimal(0)
        
        percentage_return_on_investments = (self.get_total_return_on_investments(date) / invested_capital) * 100
        return percentage_return_on_investments.quantize(
            decimal.Decimal("0.01"), rounding=decimal.ROUND_HALF_UP
        )
    
    def get_value(self, date: typing.Optional[datetime.date] = None):
        value = self.capital + self.get_total_return_on_investments(date)
        return value.quantize(
            decimal.Decimal("0.01"), rounding=decimal.ROUND_HALF_UP
        )
 

class TransactionType(models.TextChoices):
    """Available investment transaction types."""

    BUY = "buy", _("Buy")
    SELL = "sell", _("Sell")


def validate_not_in_future(value: datetime.date) -> bool:
    if value > timezone.now().date():
        raise ValidationError("Date cannot be in the future")
    return


class Investment(models.Model):
    """Model definition for an investment."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    portfolio = models.ForeignKey(
        "portfolios.Portfolio",
        on_delete=models.CASCADE,
        related_name="investments",
        db_index=True,
        null=True,
    )
    transaction_type = models.CharField(max_length=120, choices=TransactionType.choices)
    stock = models.ForeignKey(
        "stocks.Stock",
        on_delete=models.CASCADE,
        related_name="+",
        db_index=True,
        null=True,
    )
    rate = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.IntegerField()
    transaction_date = models.DateField(validators=[validate_not_in_future], null=True)
    transaction_time = models.TimeField(blank=True, null=True)
    settlement_date = models.DateField(blank=True, null=True)
    brokerage_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    ##########################
    # Additional cost fields #
    ##########################
    commission = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, blank=True, null=True
    )
    cdc = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, blank=True, null=True
    )
    psx = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, blank=True, null=True
    )
    secp = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, blank=True, null=True
    )
    nccpl = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, blank=True, null=True
    )
    cvt = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, blank=True, null=True
    )
    whts = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, blank=True, null=True
    )
    whtc = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, blank=True, null=True
    )
    adv_tax = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, blank=True, null=True
    )
    sst = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, blank=True, null=True
    )
    laga = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, blank=True, null=True
    )
    nlaga = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, blank=True, null=True
    )
    fed = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, blank=True, null=True
    )
    misc = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, blank=True, null=True
    )

    ###################
    # Metadata fields #
    ###################
    dealer = models.CharField(max_length=100, blank=True, null=True)
    client = models.CharField(max_length=100, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    residence = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    client_category = models.CharField(max_length=100, blank=True, null=True)
    cdc_id = models.CharField(max_length=100, blank=True, null=True)
    client_title = models.CharField(max_length=100, blank=True, null=True)
    flag = models.CharField(max_length=100, blank=True, null=True)
    book = models.CharField(max_length=100, blank=True, null=True)
    cot_st = models.CharField(max_length=100, blank=True, null=True)
    korder = models.CharField(max_length=100, blank=True, null=True)
    ticket = models.CharField(max_length=100, blank=True, null=True)
    terminal = models.CharField(max_length=100, blank=True, null=True)
    bill = models.CharField(max_length=100, blank=True, null=True)

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Investment")
        verbose_name_plural = _("Investments")
        ordering = ["-added_at", "-transaction_date"]

    ADDITIONAL_FEES = (
        "commission",
        "cdc",
        "psx",
        "secp",
        "nccpl",
        "cvt",
        "whts",
        "whtc",
        "adv_tax",
        "sst",
        "laga",
        "nlaga",
        "fed",
        "misc"
    )

    def __str__(self) -> str:
        return f"{self.transaction_type.upper()} {self.quantity} {self.symbol} @ {self.price}"

    # These properties are cached to avoid recalculating them every time they are accessed
    # Since they are not expected to change once the object is created
    @functools.cached_property
    def symbol(self):
        """The symbol of the stock."""
        return self.stock.ticker
    
    @functools.cached_property
    def base_principal(self):
        """The principal investment amount before any additional costs."""
        base_principal = self.rate * self.quantity
        return base_principal.quantize(
            decimal.Decimal("0.01"), rounding=decimal.ROUND_HALF_UP
        )
    
    @functools.cached_property
    def additional_fees(self):
        """The total additional fees paid on each unit of the stock invested in."""
        total = decimal.Decimal(0)
        for field in type(self).ADDITIONAL_FEES:
            fee = getattr(self, field, decimal.Decimal(0))
            # Add the value of each additional cost field to the total additional fees
            total += fee
        return total.quantize(
            decimal.Decimal("0.01"), rounding=decimal.ROUND_HALF_UP
        )
    
    @functools.cached_property
    def principal(self):
        """Capital invested before any profit or loss. Initial market value of the investment."""
        # Calculate the total fees paid on every unit of the stock invested in
        total_fees = (self.additional_fees + self.brokerage_fee) * self.quantity

        if self.transaction_type == TransactionType.SELL:
            return self.base_principal - total_fees
        return self.base_principal + total_fees

    @property
    def value(self) -> typing.Optional[decimal.Decimal]:
        """The current market value of the investment."""
        current_stock_price = self.stock.price
        if not current_stock_price:
            return None
        
        current_value = current_stock_price * self.quantity
        return current_value.quantize(
            decimal.Decimal("0.01"), rounding=decimal.ROUND_HALF_UP
        )

    @property
    def return_value(self) -> typing.Optional[decimal.Decimal]:
        """
        The current return value of the investment, either profit or loss.
        """
        value = self.value
        if not value:
            return None

        return_value = value - self.principal
        return return_value.quantize(
            decimal.Decimal("0.01"), rounding=decimal.ROUND_HALF_UP
        )
    
    @property
    def percentage_return(self) -> typing.Optional[decimal.Decimal]:
        """
        The return percentage return of the investment, either profit or loss.
        """
        return_value = self.return_value
        if not return_value:
            return None

        percentage_return = (return_value / abs(self.principal)) * 100
        return percentage_return.quantize(
            decimal.Decimal("0.01"), rounding=decimal.ROUND_HALF_UP
        )
    
    def get_value_on_date(self, date: datetime.date) -> typing.Optional[decimal.Decimal]:
        stock_price_on_date = self.stock.get_price_on_date(date)
        if not stock_price_on_date:
            return None
        
        value = stock_price_on_date * self.quantity
        return value.quantize(
            decimal.Decimal("0.01"), rounding=decimal.ROUND_HALF_UP
        )
    
    def get_return_value_on_date(self, date: datetime.date) -> typing.Optional[decimal.Decimal]:
        value = self.get_value_on_date(date)
        if not value:
            return None

        return_value = value - self.principal
        return return_value.quantize(
            decimal.Decimal("0.01"), rounding=decimal.ROUND_HALF_UP
        )
   
    def get_percentage_return_on_date(self, date: datetime.date) -> typing.Optional[decimal.Decimal]:
        """
        The current percentage return of the investment, either profit or loss.
        """
        return_value = self.get_return_value_on_date(date)
        if not return_value:
            return None

        percentage_return = (return_value / abs(self.principal)) * 100
        return percentage_return.quantize(
            decimal.Decimal("0.01"), rounding=decimal.ROUND_HALF_UP
        )
