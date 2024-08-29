import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class RiskProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        "accounts.UserAccount", related_name="risk_profiles", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    stocks = models.ManyToManyField("stocks.Stock", related_name="+", blank=True)
    criteria = models.JSONField(blank=True, null=True, default=list)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Risk Profile")
        verbose_name_plural = _("Risk Profiles")
        ordering = ["-created_at"]
