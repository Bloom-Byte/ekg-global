from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import pandas as pd
from .models import *

# Create your views here.


# @login_required
@login_required
def dashboard(request):
    return render(request, "dashboard.html")


@login_required
def portfolio_view(request):
    portfolios = Portfolio.objects.filter(user=request.user)

    if request.method == "POST":
        pf = Portfolio.objects.create(
            user=request.user,
            name=request.POST["name"],
            description=request.POST["description"],
        )

        messages.success(request, f"Portfolio '{pf.name}' Successfully Created")

    return render(request, "portfolio.html", context={"portfolios": portfolios})


@login_required
def portfolio_detail(request, pf_id):
    portfolio = Portfolio.objects.get(id=pf_id)
    trades = Trade.objects.filter(portfolio=portfolio)

    if request.method == "POST":
        Trade.objects.create(
            user=request.user,
            portfolio=portfolio,
            symbol=request.POST["symbol"],
            price=request.POST["price"],
            transaction_type=request.POST["trx_type"],
            quantity=request.POST["qty"],
            date=request.POST["date"],
        )

        messages.success(request, "Trade Successfully Added to Portfolio")

    return render(
        request, "portfolio_detail.html", context={"pf": portfolio, "trades": trades}
    )


@login_required
def rate_and_kse_upload(request):
    # create the ticker names auto in the db upon rates upload if any new are found
    # remove duplicates and then loop over ticker names from csv and cross check with db and add
    # those which do not exist
    if request.method == "POST":
        if "rate_file" in request.FILES:
            df = pd.read_csv(request.FILES["rate_file"])
            fdf = df[
                [
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
            ]

            for row in fdf.itertuples():
                Rate.objects.create(
                    ticker=row.ticker,
                    mkt=row.mkt,
                    previous_close=row.previous_close,
                    open=row.open,
                    high=row.high,
                    low=row.low,
                    close=row.close,
                    change=row.change,
                    volume=row.volume,
                )

            messages.success(request, "Rates successfully uploaded to database")

        if "kse_file" in request.FILES:
            df = pd.read_csv(request.FILES["kse_file"])
            fdf = df[["date", "open", "high", "low", "close", "volume"]]
            fdf["date"] = pd.to_datetime(fdf["date"])

            for row in fdf.itertuples():
                KSE.objects.create(
                    date=row.date,
                    open=row.open,
                    high=row.high,
                    low=row.low,
                    close=row.close,
                    volume=row.volume,
                )

            messages.success(request, "KSE successfully uploaded to database")

    return render(request, "rate_upload.html")
