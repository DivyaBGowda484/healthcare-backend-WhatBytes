# core/urls.py
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, DoctorViewSet, MappingViewSet

router = DefaultRouter()
router.register("patients", PatientViewSet, basename="patient")
router.register("doctors", DoctorViewSet, basename="doctor")
router.register("mappings", MappingViewSet, basename="mapping")

urlpatterns = router.urls
