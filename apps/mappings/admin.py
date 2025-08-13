from django.contrib import admin
from .models import PatientDoctorMapping

@admin.register(PatientDoctorMapping)
class PatientDoctorMappingAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "assigned_at", "is_active", "created_at")
    list_filter = ("doctor", "patient", "is_active")
