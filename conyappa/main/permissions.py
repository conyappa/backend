from rest_framework.permissions import BasePermission


class IsOwnerOfObject(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.owners
