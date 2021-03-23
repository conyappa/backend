from django.conf import settings

from rest_framework.permissions import SAFE_METHODS, BasePermission


class InternalCommunication(BasePermission):
    def has_permission(self, request, view):
        internal_key = request.META.get("HTTP_INTERNAL_KEY")
        return internal_key == settings.INTERNAL_KEY


class Ownership(BasePermission):
    def has_permission(self, request, view):
        user = getattr(view, "user", None)

        # Ownership over a user gives you ownership over the user’s resources.
        return self.has_object_permission(request, view, obj=user)

    def has_object_permission(self, request, view, obj=None):
        return (obj is None) or (request.user in obj.owners)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
