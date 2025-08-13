# apps/doctors/models.py
from django.db import models
from apps.core.models import TimeStampedModel

class Doctor(TimeStampedModel):
    name = models.CharField(max_length=150)
    specialization = models.CharField(max_length=150, blank=True, default="")
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, blank=True, default="")

    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"
