from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.patients.models import Patient
from apps.doctors.models import Doctor
from apps.mappings.models import PatientDoctorMapping
from .serializers import PatientSerializer, DoctorSerializer, MappingSerializer
from .permissions import IsOwnerOrAdmin, IsDoctor, IsReceptionist

def home(request):
    return render(request, 'index.html')

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.filter(is_active=True)
    serializer_class = PatientSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['age','created_at']
    search_fields = ['name','email','phone','address']
    ordering_fields = ['name','created_at','age']
    permission_classes = [IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['post'], url_path='bulk-create')
    def bulk_create(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        instances = serializer.save(created_by=request.user)
        return Response(self.get_serializer(instances, many=True).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='bulk-update')
    def bulk_update(self, request):
        payload = request.data
        updated = []
        for item in payload:
            obj = Patient.objects.filter(pk=item.get('id'), is_active=True).first()
            if not obj:
                continue
            for k,v in item.items():
                if k == 'id': continue
                setattr(obj, k, v)
            obj.updated_by = request.user
            obj.save()
            updated.append(obj)
        return Response(self.get_serializer(updated, many=True).data)

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.filter(is_active=True)
    serializer_class = DoctorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['specialization','city']
    search_fields = ['name','specialization','city']
    ordering_fields = ['name','created_at']
    permission_classes = [IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class MappingViewSet(viewsets.ModelViewSet):
    queryset = PatientDoctorMapping.objects.filter(is_active=True).select_related('doctor','patient')
    serializer_class = MappingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['patient__id','doctor__id']
    search_fields = ['doctor__name','patient__name']
    ordering_fields = ['created_at']
    permission_classes = [IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['post'])
    def bulk_assign(self, request):
        patient_ids = request.data.get("patient_ids", [])
        doctor_id = request.data.get("doctor_id")
        doctor = None
        try:
            doctor = Doctor.objects.get(pk=doctor_id, is_active=True)
        except Doctor.DoesNotExist:
            return Response({"detail":"Doctor not found"}, status=404)
        created = []
        for pid in patient_ids:
            if PatientDoctorMapping.objects.filter(patient_id=pid, doctor=doctor, is_active=True).exists():
                continue
            mapping = PatientDoctorMapping.objects.create(patient_id=pid, doctor=doctor, created_by=request.user)
            created.append(mapping)
        return Response(MappingSerializer(created, many=True).data, status=201)
