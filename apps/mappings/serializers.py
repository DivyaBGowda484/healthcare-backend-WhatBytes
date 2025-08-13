from rest_framework import serializers
from apps.mappings.models import PatientDoctorMapping
from apps.doctors.serializers import DoctorSerializer

class PatientDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = ["id", "patient", "doctor", "assigned_at"]
        read_only_fields = ["id", "assigned_at"]

class DoctorsForPatientSerializer(serializers.Serializer):
    doctors = DoctorSerializer(many=True)
