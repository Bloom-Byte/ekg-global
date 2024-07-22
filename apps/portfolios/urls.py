from django.urls import path

from . import views


app_name = "portfolios"

urlpatterns = [
    path("", views.portfolio_list_view, name="portfolio_list"),
    path("new", views.portfolio_create_view, name="portfolio_create"),
    path("<uuid:portfolio_id>", views.portfolio_detail_view, name="portfolio_detail"),
    path(
        "<uuid:portfolio_id>/delete",
        views.portfolio_delete_view,
        name="portfolio_delete",
    ),
    path(
        "<uuid:portfolio_id>/transactions/new",
        views.transaction_add_view,
        name="transaction_add",
    ),
    path(
        "<uuid:portfolio_id>/transactions/<uuid:transaction_id>/delete",
        views.transaction_delete_view,
        name="transaction_delete",
    ),
]
