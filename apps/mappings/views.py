from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import PatientDoctorSerializer, DoctorsForPatientSerializer
from apps.patients.models import Patient
from apps.doctors.models import Doctor
from apps.mappings.models import PatientDoctorMapping

class MappingViewSet(viewsets.ModelViewSet):
    queryset = PatientDoctorMapping.objects.all().order_by("-assigned_at")
    serializer_class = PatientDoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

class MappingsByPatientView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        links = PatientDoctorMapping.objects.filter(patient=patient).select_related("doctor")
        doctors = [link.doctor for link in links]
        data = {
            "doctors": [
                {
                    "id": d.id,
                    "name": d.name,
                    "specialization": d.specialization,
                    "email": d.email,
                    "phone": d.phone
                } for d in doctors
            ]
        }
        return Response(data, status=status.HTTP_200_OK)
