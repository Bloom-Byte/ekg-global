from helpers.data_utils import cleaners as cl, parsers as ps

from apps.stocks.models import Rate
from apps.stocks.helpers import get_trend


class MGLinkStockRateDataCleaner(cl.ModelDataCleaner[Rate]):
    model = Rate
    clean_strings = True
    exclude = ["id", "stock", "market", "trend", "updated_at"]
    key_mappings = {
        "ldcp": "LDCP",
        "change": "Change",
        "pct_change": "PctChange",
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "previous_close": "Last",
        "volume": "Volume",
        "added_at": "CreateDateTime",
    }

    parsers = {"added_at": [lambda v: ps.strToDateTime(v) if isinstance(v, str) else v]}

    def new_instance(self, **extra_fields):
        rate = super().new_instance(**extra_fields)

        if not extra_fields.get("trend", None):
            rate.trend = get_trend(rate.previous_close, rate.close)
        return rate
