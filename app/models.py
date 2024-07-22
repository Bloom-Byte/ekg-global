from django.db import models
from apps.accounts.models import UserAccount


# Create your models here.
class Ticker(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self) -> str:
        return self.name


class Rate(models.Model):
    ticker = models.CharField(max_length=120)
    mkt = models.CharField(max_length=120)
    previous_close = models.FloatField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    change = models.FloatField()
    volume = models.FloatField()

    def __str__(self) -> str:
        return self.ticker


class KSE(models.Model):
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()


class Portfolio(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.TextField()

    def __str__(self) -> str:
        return self.user.email


class Trade(models.Model):
    TRX_TYPE = (
        (
            "buy",
            "buy",
        ),
        (
            "sell",
            "sell",
        ),
    )

    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, related_name="pfolio", null=True
    )
    transaction_type = models.CharField(max_length=120, choices=TRX_TYPE)
    symbol = models.CharField(max_length=120, null=True)
    date = models.DateField()
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return self.user.email
