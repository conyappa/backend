from django.conf import settings
from django.contrib import admin

from .models import Movement


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    search_fields = [
        "user__email",
        "user__first_name",
        "user__last_name",
        "user__rut",
    ]

    list_display = [
        "name",
        "rut",
        "amount",
        "fintoc_post_date",
        "user",
    ]

    list_filter = [
        "fintoc_post_date",
    ]

    readonly_fields = [
        "name",
        "rut",
        "amount",
        "fintoc_post_date",
        "fintoc_data",
    ]

    fields = ["user"] + readonly_fields

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return super().has_add_permission(request) and settings.DEBUG
