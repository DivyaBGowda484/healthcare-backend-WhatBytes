# core/permissions.py
from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name="Doctor").exists()

class IsReceptionist(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name="Receptionist").exists()

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    For resources created_by — allow the creator or admins to modify, others read-only.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
        return getattr(obj, "created_by", None) == request.user
