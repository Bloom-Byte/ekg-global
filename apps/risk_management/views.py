import json
import typing 
from django.db import models
from django.views import generic
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .criteria.functions import generate_functions_schema
from .criteria.comparisons import ComparisonOperator
from helpers.exceptions import capture
from .models import RiskProfile
from .forms import RiskProfileForm


risk_profile_qs = (
    RiskProfile.objects.select_related("owner")
    .prefetch_related("stocks", "stocks__rates")
    .all()
)


class RiskManagementView(LoginRequiredMixin, generic.TemplateView):
    template_name = "risk_management/risk_management.html"

    def get_context_data(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        context_data = super().get_context_data(**kwargs)
        risk_profiles = risk_profile_qs.filter(owner=self.request.user)
        context_data["risk_profiles"] = risk_profiles

        functions_schema = generate_functions_schema(grouped=True)
        operators_schema = {op.name.replace("_", " ").upper(): op.value for op in ComparisonOperator}
        criterion_schema = {
            "functions_schema": functions_schema,
            "operators_schema": operators_schema
        }
        context_data["criterion_schema"] = criterion_schema
        return context_data
    

@capture.enable
class RiskProfileCreateView(LoginRequiredMixin, generic.View):
    http_method_names = ["post"]
    form_class = RiskProfileForm

    @capture.capture(content="Oops! An error occurred")
    def post(self, request, *args: typing.Any, **kwargs: typing.Any) -> JsonResponse:
        data: typing.Dict = json.loads(request.body)
        form = self.form_class(data=data)

        if not form.is_valid():
            return JsonResponse(
                data={
                    "status": "error",
                    "detail": "An error occurred",
                    "errors": form.errors,
                },
                status=400,
            )
        
        risk_profile = form.save(commit=False)
        risk_profile.owner = request.user
        risk_profile.save()
        return JsonResponse(
            data={
                "status": "success",
                "detail": "Risk profile created successfully",
                "redirect_url": reverse("risk_management:risk_management"),
            },
            status=200,
        )
    

@capture.enable
class RiskProfileUpdateView(LoginRequiredMixin, generic.View):
    http_method_names = ["put"]
    form_class = RiskProfileForm
    queryset = risk_profile_qs

    def get_queryset(self) -> models.QuerySet[RiskProfile]:
        user = self.request.user
        qs = self.queryset
        return qs.filter(owner=user)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), id=self.kwargs["profile_id"])

    @capture.capture(content="Oops! An error occurred")
    def put(self, request, *args: typing.Any, **kwargs: typing.Any) -> JsonResponse:
        data: typing.Dict = json.loads(request.body)
        risk_profile = self.get_object()
        form = self.form_class(data=data, instance=risk_profile)

        if not form.is_valid():
            return JsonResponse(
                data={
                    "status": "error",
                    "detail": "An error occurred",
                    "errors": form.errors,
                },
                status=400,
            )
        
        risk_profile = form.save(commit=False)
        risk_profile.owner = request.user
        risk_profile.save()
        return JsonResponse(
            data={
                "status": "success",
                "detail": "Risk profile updated successfully",
                "redirect_url": reverse("risk_management:risk_management"),
            },
            status=200,
        )


class RiskProfileDeleteView(LoginRequiredMixin, generic.View):
    queryset = risk_profile_qs
    http_method_names = ["get"]

    def get_queryset(self) -> models.QuerySet[RiskProfile]:
        user = self.request.user
        qs = self.queryset
        return qs.filter(owner=user)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), id=self.kwargs["profile_id"])

    def get(self, request, *args, **kwargs):
        risk_profile = self.get_object()
        risk_profile.delete()
        return redirect(self.get_success_url())

    def get_success_url(self) -> str:
        return reverse("risk_management:risk_management")


risk_management_view = RiskManagementView.as_view()
risk_profile_create_view = RiskProfileCreateView.as_view()
risk_profile_update_view = RiskProfileUpdateView.as_view()
risk_profile_delete_view = RiskProfileDeleteView.as_view()

