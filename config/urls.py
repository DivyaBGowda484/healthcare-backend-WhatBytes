from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.patients.views import PatientViewSet
from apps.doctors.views import DoctorViewSet
from apps.mappings.views import MappingViewSet, MappingsByPatientView
from apps.core.views import home

router = DefaultRouter()
router.register(r"patients", PatientViewSet, basename="patient")
router.register(r"doctors", DoctorViewSet, basename="doctor")
router.register(r"mappings", MappingViewSet, basename="mapping")

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home, name='home'),
    path("api/", include(router.urls)),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/mappings/by-patient/<int:patient_id>/", MappingsByPatientView.as_view(), name="mappings-by-patient"),
]
