import json
import typing 
from django.db import models
from django.views import generic
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from helpers.exceptions import capture
from .models import RiskProfile
from .forms import RiskProfileCreateForm


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
        return context_data
    

@capture.enable
class RiskProfileCreateView(LoginRequiredMixin, generic.View):
    http_method_names = ["post"]
    form_class = RiskProfileCreateForm

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


risk_management_view = RiskManagementView.as_view()
