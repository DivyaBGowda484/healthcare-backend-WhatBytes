from django.conf import settings
from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        related_name="%(class)s_created", on_delete=models.SET_NULL
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        related_name="%(class)s_updated", on_delete=models.SET_NULL
    )
    is_active = models.BooleanField(default=True)  # Soft delete flag

    class Meta:
        abstract = True
