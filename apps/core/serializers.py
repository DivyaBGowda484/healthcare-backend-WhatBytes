from rest_framework import serializers
from apps.patients.models import Patient
from apps.doctors.models import Doctor
from apps.mappings.models import PatientDoctorMapping

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"
        read_only_fields = ("created_at","updated_at","created_by","updated_by","is_active")

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"
        read_only_fields = ("created_at","updated_at","created_by","updated_by","is_active")

    def validate_phone(self, value):
        if value:
            digits = ''.join(ch for ch in value if ch.isdigit())
            if len(digits) < 7:
                raise serializers.ValidationError("Phone number is too short")
        return value

    def validate_email(self, value):
        return value

class MappingSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.filter(is_active=True), source="doctor", write_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.filter(is_active=True), source="patient", write_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ("id","patient_id","doctor_id","doctor","created_at","created_by")
        read_only_fields = ("created_at","created_by","doctor")

    def validate(self, data):
        patient = data.get("patient")
        doctor = data.get("doctor")
        if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor, is_active=True).exists():
            raise serializers.ValidationError("This doctor is already assigned to the patient.")
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        mapping = PatientDoctorMapping.objects.create(**validated_data)
        if request and request.user.is_authenticated:
            mapping.created_by = request.user
            mapping.save()
        return mapping
