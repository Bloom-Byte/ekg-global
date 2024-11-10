from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect
from django.views import generic


class IndexView(generic.TemplateView):
    template_name = "dashboard/index.html"
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect("accounts:signin")
        return super().get(request, *args, **kwargs)


index_view = IndexView.as_view()
