from django.views import generic


class RiskManagementView(generic.TemplateView):
    template_name = 'risk_management/risk_management.html'


risk_management_view = RiskManagementView.as_view()
