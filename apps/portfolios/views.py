from typing import Any, Dict
import json
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import Portfolio, Transaction
from apps.stocks.models import Stock
from .forms import PortfolioCreateForm, TransactionAddForm
from helpers.exceptions import capture


portfolio_qs = Portfolio.objects.select_related("owner").all()
transaction_qs = Transaction.objects.all()


class PortfolioListView(LoginRequiredMixin, generic.ListView):
    context_object_name = "portfolios"
    # paginate_by = 20
    queryset = portfolio_qs
    template_name = "portfolios/portfolio_list.html"

    def get_queryset(self) -> QuerySet[Portfolio]:
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(owner=user)


@capture.enable
class PortfolioCreateView(LoginRequiredMixin, generic.View):
    http_method_names = ["post"]
    form_class = PortfolioCreateForm

    @capture.capture(content="Oops! An error occurred")
    def post(self, request, *args: Any, **kwargs: Any) -> JsonResponse:
        data: Dict = json.loads(request.body)
        form = self.form_class(data={"owner": request.user, **data})

        if not form.is_valid():
            return JsonResponse(
                data={
                    "status": "error",
                    "detail": "An error occurred",
                    "errors": form.errors,
                },
                status=400,
            )
        form.save()
        return JsonResponse(
            data={
                "status": "success",
                "detail": "Portfolio created successfully",
                "redirect_url": reverse("portfolios:portfolio_list"),
            },
            status=200,
        )


class PortfolioDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "portfolios/portfolio_detail.html"
    queryset = portfolio_qs
    pk_url_kwarg = "portfolio_id"
    context_object_name = "portfolio"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["stocks"] = Stock.objects.all()
        return context

    def get_queryset(self) -> QuerySet[Portfolio]:
        user = self.request.user
        qs = super().get_queryset()
        return qs.prefetch_related("transactions").filter(owner=user)


class PortfolioDeleteView(LoginRequiredMixin, generic.View):
    queryset = portfolio_qs
    http_method_names = ["get"]

    def get_queryset(self) -> QuerySet[Portfolio]:
        user = self.request.user
        qs = self.queryset
        return qs.filter(owner=user)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), id=self.kwargs["portfolio_id"])

    def get(self, request, *args, **kwargs):
        portfolio = self.get_object()
        portfolio.delete()
        return redirect(self.get_success_url())

    def get_success_url(self) -> str:
        return reverse("portfolios:portfolio_list")


@capture.enable
class TransactionAddView(LoginRequiredMixin, generic.View):
    http_method_names = ["post"]
    form_class = TransactionAddForm

    @capture.capture(content="Oops! An error occurred")
    def post(self, request, *args: Any, **kwargs: Any) -> JsonResponse:
        data: Dict = json.loads(request.body)
        portfolio_id = self.kwargs["portfolio_id"]
        data.update(
            {
                "portfolio": portfolio_id,
            }
        )
        form = self.form_class(data)

        if not form.is_valid():
            return JsonResponse(
                data={
                    "status": "error",
                    "detail": "An error occurred",
                    "errors": form.errors,
                },
                status=400,
            )
        form.save()
        return JsonResponse(
            data={
                "status": "success",
                "detail": "Transaction added successfully",
                "redirect_url": reverse(
                    "portfolios:portfolio_detail", kwargs={"portfolio_id": portfolio_id}
                ),
            },
            status=200,
        )


class TransactionDeleteView(LoginRequiredMixin, generic.View):
    queryset = transaction_qs
    http_method_names = ["get"]

    def get_queryset(self) -> QuerySet[Transaction]:
        user = self.request.user
        portfolio_id = self.kwargs["portfolio_id"]
        qs = self.queryset
        return qs.filter(portfolio_id=portfolio_id, portfolio__owner=user)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), id=self.kwargs["transaction_id"])

    def get(self, request, *args, **kwargs):
        transaction = self.get_object()
        transaction.delete()
        return redirect(self.get_success_url())

    def get_success_url(self) -> str:
        return reverse(
            "portfolios:portfolio_detail",
            kwargs={"portfolio_id": self.kwargs["portfolio_id"]},
        )


portfolio_list_view = PortfolioListView.as_view()
portfolio_create_view = PortfolioCreateView.as_view()
portfolio_detail_view = PortfolioDetailView.as_view()
portfolio_delete_view = PortfolioDeleteView.as_view()

transaction_add_view = TransactionAddView.as_view()
transaction_delete_view = TransactionDeleteView.as_view()
