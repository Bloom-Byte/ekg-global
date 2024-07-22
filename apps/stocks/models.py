import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Stock(models.Model):
    """Model definition for Stock."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticker = models.CharField(max_length=120, unique=True)

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Stock")
        verbose_name_plural = _("Stocks")
        ordering = ["-added_at"]

    def __str__(self) -> str:
        return self.ticker


class MarketType(models.TextChoices):
    REGULAR = "REG", _("Regular")
    FUTURE = "FUT", _("Future")
    ODD_LOT = "ODL", _("Odd Lot")


class MarketTrend(models.TextChoices):
    UP = "up", _("Up")
    DOWN = "down", _("Down")
    NEUTRAL = "neutral", _("Neutral")


class Rate(models.Model):
    """Model definition for a Rate."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stock = models.OneToOneField(
        "stocks.Stock", on_delete=models.CASCADE, related_name="rate"
    )
    market = models.CharField(max_length=20, choices=MarketType.choices)
    previous_close = models.FloatField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    trend = models.CharField(
        max_length=10, choices=MarketTrend.choices, default=MarketTrend.NEUTRAL
    )
    change = models.FloatField()
    volume = models.FloatField()

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Rate")
        verbose_name_plural = _("Rates")
        ordering = ["-added_at"]
