import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomRiskProfile(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    stocks = models.ManyToManyField(
        "stocks.Stock", related_name="+", blank=True
    )
    metadata = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Custom Risk Profile")
        verbose_name_plural = _("Custom Risk Profiles")
        ordering = ["-created_at"]
