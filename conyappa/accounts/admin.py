from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from admin_numeric_filter.admin import NumericFilterModelAdmin, SliderNumericFilter

from banking.models import Movement
from lottery.models import Ticket

from .models import User


class TicketInline(admin.TabularInline):
    model = Ticket

    readonly_fields = ["picks"]
    fields = ["picks", "draw"]
    extra = 0

    classes = ["collapse"]

    def has_view_or_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class MovementInline(admin.TabularInline):
    model = Movement

    readonly_fields = ["rut", "fintoc_post_date"]
    fields = [tuple(readonly_fields)]
    extra = 0

    classes = ["collapse"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class UserBalanceChangeForm(admin.helpers.ActionForm):
    amount = forms.IntegerField(min_value=0, max_value=1000000)


@admin.register(User)
class UserAdmin(NumericFilterModelAdmin):
    action_form = UserBalanceChangeForm

    actions = [
        "deposit",
        "withdraw",
    ]

    search_fields = [
        "email",
        "first_name",
        "last_name",
        "rut",
    ]

    list_display = [
        "email",
        "full_name",
        "formatted_rut",
        "balance",
        "winnings",
        "is_staff",
        "is_superuser",
    ]

    list_filter = [
        "is_staff",
        "is_superuser",
        "date_joined",
        ("balance", SliderNumericFilter),
        ("winnings", SliderNumericFilter),
    ]

    fieldsets = [
        (
            "PERMISSIONS",
            {
                "fields": [
                    "is_staff",
                    "is_superuser",
                    "groups",
                ],
                "classes": ["collapse"],
            },
        ),
        (
            "PERSONAL",
            {
                "fields": [
                    "email",
                    ("rut", "check_digit"),
                    ("first_name", "last_name"),
                ],
                "classes": ["collapse"],
            },
        ),
        (
            "FINANCIAL",
            {
                "fields": [
                    ("balance", "winnings", "current_prize"),
                    ("current_number_of_tickets", "extra_tickets_ttl"),
                ],
                "classes": ["collapse"],
            },
        ),
    ]

    readonly_fields = [
        "email",
        "balance",
        "winnings",
        "current_number_of_tickets",
        "current_prize",
    ]

    check_digit = None

    inlines = [TicketInline, MovementInline]

    def has_add_permission(self, request):
        return super().has_add_permission(request) and settings.DEBUG

    def has_delete_permission(self, request, obj=None):
        return super().has_add_permission(request) and settings.DEBUG

    @staticmethod
    def log_change(request, user, message):
        content_type = ContentType.objects.get_for_model(user)

        LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=content_type.pk,
            object_id=user.pk,
            object_repr=str(user),
            action_flag=CHANGE,
            change_message=message,
        )

    @transaction.atomic
    def deposit(self, request, queryset):
        amount = int(request.POST["amount"])

        for user in queryset:
            user.deposit(amount)
            self.log_change(request, user, message=f"Deposited {amount}")

    @transaction.atomic
    def withdraw(self, request, queryset):
        amount = int(request.POST["amount"])

        for user in queryset:
            user.withdraw(amount)
            self.log_change(request, user, message=f"Withdrawed {amount}")
