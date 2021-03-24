from django.conf import settings
from django.contrib import admin

from .models import Movement


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
        "raw_rut",
        "user__email",
        "user__first_name",
        "user__last_name",
        "user__rut",
    ]

    list_display = [
        "name",
        "raw_rut",
        "user",
        "amount",
        "fintoc_post_date",
    ]

    list_filter = [
        "fintoc_post_date",
    ]

    readonly_fields = [
        "name",
        "raw_rut",
        "fintoc_data",
        "fintoc_post_date",
        "amount",
    ]

    fields = ["user"] + readonly_fields

    def has_add_permission(self, request):
        return super().has_add_permission(request) and settings.DEBUG

    def has_delete_permission(self, request, obj=None):
        return super().has_add_permission(request) and settings.DEBUG
