from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "specialization", "created_at")
    search_fields = ("name", "email", "specialization")
    list_filter = ("specialization",)
