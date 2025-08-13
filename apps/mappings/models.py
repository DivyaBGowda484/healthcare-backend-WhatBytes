from django.db import models
from apps.core.models import TimeStampedModel

class PatientDoctorMapping(TimeStampedModel):
    patient = models.ForeignKey("patients.Patient", on_delete=models.CASCADE, related_name="doctor_links")
    doctor = models.ForeignKey("doctors.Doctor", on_delete=models.CASCADE, related_name="patient_links")
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("patient", "doctor")

    def __str__(self):
        return f"{self.patient} -> {self.doctor}"
