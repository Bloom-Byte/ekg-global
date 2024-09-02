from django.urls import path

from . import views

app_name = "risk_management"


urlpatterns = [
    path("", views.risk_management_view, name="risk_management"),
    path(
        "criteria-creation-schema",
        views.criteria_creation_schema_view,
        name="criteria_creation_schema",
    ),
]
