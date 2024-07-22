import decimal
import uuid
import math
import datetime
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
    cash_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    brokerage_percentage = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True
    )
    description = models.TextField(null=True, blank=True)

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
    def balance(self):
        return self.cash_amount - self.total_expenditure

    @property
    def total_expenditure(self):
        return decimal.Decimal.from_float(math.fsum(self.expenditures())).quantize(
            decimal.Decimal("0.001"), rounding=decimal.ROUND_HALF_UP
        )

    def expenditures(self):
        for transaction in self.transactions.all():
            yield transaction.gross_cost


class TransactionType(models.TextChoices):
    """Available transaction types."""

    BUY = "buy", _("Buy")
    SELL = "sell", _("Sell")


def validate_not_in_future(value: datetime.date) -> bool:
    if value > timezone.now().date():
        raise ValidationError("Date cannot be in the future")
    return


class Transaction(models.Model):
    """Model definition for transaction."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    portfolio = models.ForeignKey(
        "portfolios.Portfolio",
        on_delete=models.CASCADE,
        related_name="transactions",
        db_index=True,
        null=True,
    )
    type = models.CharField(max_length=120, choices=TransactionType.choices)
    stock = models.ForeignKey(
        "stocks.Stock",
        on_delete=models.CASCADE,
        related_name="+",
        db_index=True,
        null=True,
    )
    date = models.DateField(validators=[validate_not_in_future])
    price = models.DecimalField(max_digits=12, decimal_places=5)
    quantity = models.IntegerField()
    brokerage_fee = models.DecimalField(max_digits=12, decimal_places=5, default=0)
    commission = models.DecimalField(
        max_digits=12, decimal_places=5, default=0, blank=True, null=True
    )
    cdc = models.DecimalField(
        max_digits=12, decimal_places=5, default=0, blank=True, null=True
    )
    psx_laga = models.DecimalField(
        max_digits=12, decimal_places=5, default=0, blank=True, null=True
    )
    secp_laga = models.DecimalField(
        max_digits=12, decimal_places=5, default=0, blank=True, null=True
    )
    nccpl = models.DecimalField(
        max_digits=12, decimal_places=5, default=0, blank=True, null=True
    )
    cvt = models.DecimalField(
        max_digits=12, decimal_places=5, default=0, blank=True, null=True
    )
    wht = models.DecimalField(
        max_digits=12, decimal_places=5, default=0, blank=True, null=True
    )
    adv_tax = models.DecimalField(
        max_digits=12, decimal_places=5, default=0, blank=True, null=True
    )
    sst = models.DecimalField(
        max_digits=12, decimal_places=5, default=0, blank=True, null=True
    )

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
        ordering = ["-added_at"]

    ADDITIONAL_COST_FIELDS = (
        "commission",
        "cdc",
        "psx_laga",
        "secp_laga",
        "nccpl",
        "cvt",
        "wht",
        "adv_tax",
        "sst",
    )

    def __str__(self) -> str:
        return f"{self.type.upper()} {self.quantity} {self.symbol} @ {self.price}"

    @property
    def net_cost(self):
        return self.price * self.quantity

    @property
    def gross_cost(self):
        return self.get_gross_cost()

    def get_gross_cost(self):
        additional_cost = self.brokerage_fee
        for field in type(self).ADDITIONAL_COST_FIELDS:
            additional_cost += getattr(self, field, decimal.Decimal(0))

        if self.type == TransactionType.SELL:
            return self.net_cost - additional_cost
        return self.net_cost + additional_cost
