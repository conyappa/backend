from django.contrib import admin
from .models import Rule


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
    ]

    list_display = [
        "name",
        "updated_at",
    ]

    list_filter = [
        "updated_at",
    ]

    fields = [
        "name",
    ]
