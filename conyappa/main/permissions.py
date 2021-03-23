from django.conf import settings

from rest_framework.permissions import SAFE_METHODS, BasePermission


class InternalCommunication(BasePermission):
    def has_permission(self, request, view):
        internal_key = request.META.get("HTTP_INTERNAL_KEY")
        return internal_key == settings.INTERNAL_KEY


class OwnerOfObject(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.owners


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
