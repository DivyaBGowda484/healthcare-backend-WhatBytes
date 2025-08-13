from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """Allow access only to objects owned by the requesting user."""
    def has_object_permission(self, request, view, obj):
        owner = getattr(obj, "created_by", None)
        return owner == request.user
