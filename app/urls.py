from django.urls import path
from .views import *


urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("uploads/", rate_and_kse_upload, name="uploads"),
    path("portfolio/", portfolio_view, name="portfolio"),
    path("view-portfolio/<int:pf_id>", portfolio_detail, name="portfolio_detail"),
]
