from django.conf import settings
from django.contrib import admin

from .models import Draw, Ticket


@admin.register(Draw)
class DrawAdmin(admin.ModelAdmin):
    list_display = [
        "start_date",
        "results",
    ]

    list_filter = [
        "start_date",
    ]

    readonly_fields = [
        "start_date",
        "pool",
        "results",
    ]

    def has_add_permission(self, request):
        return super().has_add_permission(request) and settings.DEBUG

    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj) and settings.DEBUG

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj) and settings.DEBUG


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    search_fields = [
        "user__email",
        "user__first_name",
        "user__last_name",
        "user__rut",
    ]

    readonly_fields = [
        "picks",
        "draw",
        "user",
    ]

    list_display = [
        "user",
        "draw",
        "picks",
    ]

    list_filter = [
        "draw",
    ]

    def has_add_permission(self, request):
        return super().has_add_permission(request) and settings.DEBUG

    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj) and settings.DEBUG

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj) and settings.DEBUG
