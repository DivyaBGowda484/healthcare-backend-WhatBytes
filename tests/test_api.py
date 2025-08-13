# tests/test_api.py
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from apps.patients.models import Patient
from apps.doctors.models import Doctor
from apps.mappings.models import PatientDoctorMapping
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class APICriticalTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.doctor = Doctor.objects.create(name="Dr A", specialization="Cardio", email="drA@example.com")
        self.patient = Patient.objects.create(
            name="John Doe",
            age=30,
            gender="M",
            created_by=self.user
        )

        # Generate JWT token and set Authorization header
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_patient_creation(self):
        url = "/api/patients/"
        payload = {"name": "Alice", "age": 25, "gender": "F"}
        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["name"], "Alice")

    def test_mapping_duplicate_prevented(self):
        url = "/api/mappings/"
        payload = {"patient": self.patient.id, "doctor": self.doctor.id}

        r1 = self.client.post(url, payload, format="json")
        self.assertEqual(r1.status_code, status.HTTP_201_CREATED)

        r2 = self.client.post(url, payload, format="json")
        self.assertEqual(r2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", r2.data)
        self.assertIn("must make a unique set", str(r2.data))
# tests/test_api.py
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from apps.patients.models import Patient
from apps.doctors.models import Doctor
from apps.mappings.models import PatientDoctorMapping
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class APICriticalTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.doctor = Doctor.objects.create(name="Dr A", specialization="Cardio", email="drA@example.com")
        self.patient = Patient.objects.create(
            name="John Doe",
            age=30,
            gender="M",
            created_by=self.user
        )

        # Generate JWT token and set Authorization header
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_patient_creation(self):
        url = "/api/patients/"
        payload = {"name": "Alice", "age": 25, "gender": "F"}
        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["name"], "Alice")

    def test_mapping_duplicate_prevented(self):
        url = "/api/mappings/"
        payload = {"patient": self.patient.id, "doctor": self.doctor.id}

        r1 = self.client.post(url, payload, format="json")
        self.assertEqual(r1.status_code, status.HTTP_201_CREATED)

        r2 = self.client.post(url, payload, format="json")
        self.assertEqual(r2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", r2.data)
        self.assertIn("must make a unique set", str(r2.data))
