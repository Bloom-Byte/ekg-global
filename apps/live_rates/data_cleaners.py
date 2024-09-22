from helpers.data_utils import cleaners as cl
from dateutil.parser import parse as parse_date

from apps.stocks.models import Rate
from apps.stocks.helpers import get_trend


class MGLinkStockRateDataCleaner(cl.ModelDataCleaner[Rate]):
    model = Rate
    exclude = ["id", "stock", "market", "trend", "updated_at"]
    key_mappings = {
        "added_at": "create_date_time",
    }
    parsers = {"added_at": [lambda v: parse_date(v) if isinstance(v, str) else v]}

    def new_instance(self, **extra_fields):
        rate = super().new_instance(**extra_fields)

        if not extra_fields.get("trend", None):
            rate.trend = get_trend(rate.previous_close, rate.close)
        return rate
