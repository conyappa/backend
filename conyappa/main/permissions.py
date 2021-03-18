from django.conf import settings

from rest_framework.permissions import BasePermission


class IsOwnerOfObject(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.owners


class InternalCommunication(BasePermission):
    def has_permission(self, request, view):
        internal_key = request.META.get("HTTP_INTERNAL_KEY")
        return internal_key == settings.INTERNAL_KEY
