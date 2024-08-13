from django.contrib import admin
from django.conf import settings
from django.urls import path, include


urlpatterns = [
    path("", include("apps.dashboard.urls", namespace="dashboard")),
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls", namespace="accounts")),
    path("stocks/", include("apps.stocks.urls", namespace="stocks")),
    path("portfolios/", include("apps.portfolios.urls", namespace="portfolios")),
]

admin.site.site_header = f"{settings.APPLICATION_NAME} Admin"
admin.site.site_title = f"{settings.APPLICATION_ALIAS} Admin"
