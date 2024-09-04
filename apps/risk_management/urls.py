from django.urls import path

from . import views

app_name = "risk_management"


urlpatterns = [
    path("", views.risk_management_view, name="risk_management"),
    path("create-risk-profile/", views.risk_profile_create_view, name="risk_profile_create"),
]
