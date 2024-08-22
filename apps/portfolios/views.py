from typing import Any, Dict
import json
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import Portfolio, Investment
from apps.stocks.models import Stock
from .forms import PortfolioCreateForm, InvestmentAddForm, PortfolioUpdateForm
from helpers.exceptions import capture
from helpers.logging import log_exception
from .helpers import (
    get_investments_allocation_piechart_data,
    get_portfolio_performance_graph_data,
    get_stocks_invested_from_investments,
    handle_transactions_file,
    get_transactions_upload_template,
    generate_portfolio_stock_profiles,
)

portfolio_qs = (
    Portfolio.objects.select_related("owner")
    .prefetch_related("investments", "investments__stock", "investments__stock__rates")
    .all()
)
investment_qs = (
    Investment.objects.select_related("portfolio", "stock")
    .prefetch_related("stock__rates")
    .all()
)
stock_qs = Stock.objects.prefetch_related("rates").all()


class PortfolioListView(LoginRequiredMixin, generic.ListView):
    context_object_name = "portfolios"
    paginate_by = 30
    queryset = portfolio_qs
    template_name = "portfolios/portfolio_list.html"
    http_method_names = ["get", "post"]

    def get_queryset(self) -> QuerySet[Portfolio]:
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(owner=user)

    def post(self, request, *args, **kwargs):
        transactions_file = request.FILES.get("transactions_file", None)
        try:
            if transactions_file:
                handle_transactions_file(transactions_file, request.user)
                messages.success(request, "Transactions upload successful.")
        except Exception as exc:
            log_exception(exc)
            messages.error(request, "Upload failed! Check the file and try again.")

        return redirect("portfolios:portfolio_list")


class TransactionsUploadTemplateDownloadView(generic.View):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        template = get_transactions_upload_template()

        if not template:
            return HttpResponse(status=404)
        headers = {
            "Content-Disposition": f"attachment; filename={template.name}",
            "Content-Type": template.content_type,
        }
        return HttpResponse(content=template, headers=headers, status=200)


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


# Use list view for detail view so Investments can be paginated.
# Instead, add the portfolio to the context
class PortfolioDetailView(LoginRequiredMixin, generic.ListView):
    template_name = "portfolios/portfolio_detail.html"
    queryset = investment_qs
    paginate_by = 200
    context_object_name = "investments"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        investments = context["investments"]
        portfolio = get_object_or_404(
            portfolio_qs, id=self.kwargs["portfolio_id"], owner=self.request.user
        )
        stock_profile_dt_filter = self.request.GET.get("filter_sp_by", "5D")

        context["portfolio"] = portfolio
        context["all_stocks"] = stock_qs
        context["invested_stocks"] = get_stocks_invested_from_investments(investments)
        context["pie_chart_data"] = json.dumps(
            get_investments_allocation_piechart_data(investments)
        )

        # Performance data is no longer calculated and sent pre-page load
        # as it is it very costly and increases page load time (even with query optimizations)
        # Hence, client should fetch performance data via the `PortfolioPerformanceDataView` after the page loads
        # context["line_chart_data"] = json.dumps(
        #     get_portfolio_performance_graph_data(portfolio)
        # )
        context["stock_profiles"] = generate_portfolio_stock_profiles(
            portfolio, dt_filter=stock_profile_dt_filter
        )
        context["stock_profiles_dt_filter"] = stock_profile_dt_filter
        return context

    def get_queryset(self) -> QuerySet[Portfolio]:
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(
            portfolio_id=self.kwargs["portfolio_id"], portfolio__owner=user
        )


@capture.enable
@capture.capture(content="Oops! An error occurred")
class PortfolioPerformanceDataView(LoginRequiredMixin, generic.View):
    http_method_names = ["post"]

    def get_object(self):
        # Note that the portfolio queryset is used not the model.
        # This is because the queryset has prefetched and selected related data
        # Making it way more efficient that using the model
        return get_object_or_404(portfolio_qs, id=self.kwargs["portfolio_id"])

    def post(self, request, *args: Any, **kwargs: Any) -> JsonResponse:
        data: Dict = json.loads(request.body)
        dt_filter = data.get("dt_filter", "5D")
        stocks = data.get("stocks", None)
        timezone = data.get("timezone", None)
        portfolio = self.get_object()
        data = get_portfolio_performance_graph_data(
            portfolio=portfolio,
            dt_filter=dt_filter,
            stocks=stocks,
            timezone=timezone,
        )
        return JsonResponse(
            data={
                "status": "success",
                "detail": "Performance data fetched successfully",
                "data": data,
            },
            status=200,
        )


@capture.enable
@capture.capture(content="Oops! An error occurred")
class PortfolioUpdateView(LoginRequiredMixin, generic.View):
    http_method_names = ["patch"]
    form_class = PortfolioUpdateForm

    def get_object(self):
        return get_object_or_404(portfolio_qs, id=self.kwargs["portfolio_id"])

    def patch(self, request, *args: Any, **kwargs: Any) -> JsonResponse:
        data: Dict = json.loads(request.body)
        form = self.form_class(data=data, instance=self.get_object())

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
                "detail": "Portfolio updated successfully",
                "redirect_url": reverse("portfolios:portfolio_list"),
            },
            status=200,
        )


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
class InvestmentAddView(LoginRequiredMixin, generic.View):
    http_method_names = ["post"]
    form_class = InvestmentAddForm

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
                "detail": "Investment added successfully",
                "redirect_url": reverse(
                    "portfolios:portfolio_detail", kwargs={"portfolio_id": portfolio_id}
                ),
            },
            status=200,
        )


class InvestmentDeleteView(LoginRequiredMixin, generic.View):
    queryset = investment_qs
    http_method_names = ["get"]

    def get_queryset(self) -> QuerySet[Investment]:
        user = self.request.user
        portfolio_id = self.kwargs["portfolio_id"]
        qs = self.queryset
        return qs.filter(portfolio_id=portfolio_id, portfolio__owner=user)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), id=self.kwargs["investment_id"])

    def get(self, request, *args, **kwargs):
        investment = self.get_object()
        investment.delete()
        return redirect(self.get_success_url())

    def get_success_url(self) -> str:
        return reverse(
            "portfolios:portfolio_detail",
            kwargs={"portfolio_id": self.kwargs["portfolio_id"]},
        )


portfolio_list_view = PortfolioListView.as_view()
transactions_upload_template_download_view = (
    TransactionsUploadTemplateDownloadView.as_view()
)
portfolio_create_view = PortfolioCreateView.as_view()
portfolio_detail_view = PortfolioDetailView.as_view()
portfolio_performance_data_view = PortfolioPerformanceDataView.as_view()
portfolio_update_view = PortfolioUpdateView.as_view()
portfolio_delete_view = PortfolioDeleteView.as_view()

investment_add_view = InvestmentAddView.as_view()
investment_delete_view = InvestmentDeleteView.as_view()
