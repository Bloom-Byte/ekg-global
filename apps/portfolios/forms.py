from django import forms
import decimal
import typing

from .models import Portfolio, Transaction
from apps.stocks.models import Stock


class PortfolioCreateForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ("owner", "name", "cash_amount", "brokerage_percentage", "description")


ModelForm = typing.TypeVar("ModelForm", bound=forms.ModelForm)


def _clean_percentage_to_decimal(fields: typing.List[str]):
    def make_clean_method_for_field(field: str):
        def _clean_method(form: ModelForm):
            value: str = form.cleaned_data[field]
            if not value:
                return decimal.Decimal(0)
            if value.endswith("%"):
                price = form.cleaned_data["price"]
                value = (decimal.Decimal(value.removesuffix("%")) / 100) * price
            # Round to five decimal places
            return decimal.Decimal(value).quantize(
                decimal.Decimal("0.00001"), rounding=decimal.ROUND_HALF_UP
            )

        _clean_method.__name__ = f"clean_{field}"
        _clean_method.__qualname__ = f"clean_{field}"
        return _clean_method

    def form_class_decorator(form_class: typing.Type[ModelForm]):
        for field in fields:
            if field not in form_class._meta.fields:
                continue
            setattr(form_class, f"clean_{field}", make_clean_method_for_field(field))
        return form_class

    return form_class_decorator


@_clean_percentage_to_decimal((*Transaction.ADDITIONAL_COST_FIELDS, "brokerage_fee"))
class TransactionAddForm(forms.ModelForm):
    portfolio = forms.UUIDField()
    stock = forms.CharField()
    brokerage_fee = forms.CharField(required=True, strip=True)
    commission = forms.CharField(required=False, strip=True)
    cdc = forms.CharField(required=False, strip=True)
    psx_laga = forms.CharField(required=False, strip=True)
    secp_laga = forms.CharField(required=False, strip=True)
    nccpl = forms.CharField(required=False, strip=True)
    cvt = forms.CharField(required=False, strip=True)
    wht = forms.CharField(required=False, strip=True)
    adv_tax = forms.CharField(required=False, strip=True)
    sst = forms.CharField(required=False, strip=True)

    class Meta:
        model = Transaction
        fields = (
            "portfolio",
            "type",
            "stock",
            "date",
            "price",
            "quantity",
            "brokerage_fee",
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

    def clean_portfolio(self):
        portfolio = self.cleaned_data["portfolio"]
        try:
            portfolio = Portfolio.objects.get(id=portfolio)
        except Portfolio.DoesNotExist as exc:
            raise forms.ValidationError(str(exc))
        return portfolio

    def clean_stock(self):
        stock = self.cleaned_data["stock"]
        try:
            stock = Stock.objects.get(ticker=stock)
        except Stock.DoesNotExist as exc:
            raise forms.ValidationError(str(exc))
        return stock
