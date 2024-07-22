from typing import Dict, Any
import json
from django.views import generic
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .helpers import handle_rates_file, get_stock_latest_price
from helpers.logging import log_exception
from helpers.exceptions import capture


class UploadsView(LoginRequiredMixin, generic.TemplateView):
    http_method_names = ["get", "post"]
    template_name = "stocks/uploads.html"

    def post(self, request, *args, **kwargs):
        rates_file = request.FILES.get("rates_file", None)
        try:
            if rates_file:
                success = handle_rates_file(rates_file)
                if success:
                    messages.success(request, "Rates uploaded successfully.")
                else:
                    messages.error(request, "Rate upload failed.")
        except Exception as exc:
            log_exception(exc)
            messages.error(request, "Upload failed. Check the file and try again.")

        return super().get(request, *args, **kwargs)


@capture.enable
class StockLatestPriceView(LoginRequiredMixin, generic.View):
    http_method_names = ["post"]

    @capture.capture(content="Oops! An error occurred")
    def post(self, request, *args: Any, **kwargs: Any) -> JsonResponse:
        data: Dict = json.loads(request.body)
        ticker = data["stock"]
        latest_price = get_stock_latest_price(ticker)
        if latest_price is None:
            return JsonResponse(
                data={
                    "status": "error",
                    "detail": "No price found",
                },
                status=417,
            )

        return JsonResponse(
            data={
                "status": "success",
                "detail": "Price fetched successfully",
                "data": {
                    "latest_price": latest_price,
                },
            },
            status=200,
        )


uploads_view = UploadsView.as_view()
stock_latest_price_view = StockLatestPriceView.as_view()
