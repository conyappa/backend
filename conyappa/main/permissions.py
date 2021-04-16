from django.conf import settings

from rest_framework.permissions import SAFE_METHODS, BasePermission


class InternalCommunication(BasePermission):
    def has_permission(self, request, view):
        internal_key = request.META.get("HTTP_INTERNAL_KEY")
        return internal_key == settings.INTERNAL_KEY


class ObjectOwnership(BasePermission):
    def has_object_permission(self, request, view, obj=None):
        return (obj is not None) and (request.user in obj.owners)


class ListOwnership(BasePermission):
    def has_permission(self, request, view):
        user = getattr(view, "user", None)

        # Ownership over a user gives you ownership over the user’s resources.
        return (user is not None) and ObjectOwnership().has_object_permission(request, view, obj=user)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
