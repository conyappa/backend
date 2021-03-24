from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import F

from admin_numeric_filter.admin import NumericFilterModelAdmin, SliderNumericFilter
from lottery.models import Draw, Ticket
from banking.models import Movement

from .models import User


class TicketInline(admin.TabularInline):
    model = Ticket

    readonly_fields = ["draw"]
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

    classes = ['collapse']

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
        ("PERSONAL", {
            "fields": [
                "email",
                ("rut", "check_digit"),
                ("first_name", "last_name"),
            ],
            "classes": ["collapse"],
        }),
        ("FINANCIAL", {
            "fields": [
                ("balance", "winnings", "current_prize"),
                ("number_of_current_tickets", "extra_tickets_ttl"),
            ],
            "classes": ["collapse"],
        })
    ]

    readonly_fields = [
        "email",
        "number_of_current_tickets",
        "current_prize",
        "balance",
        "winnings",
    ]

    check_digit = None

    inlines = [TicketInline, MovementInline]

    def has_add_permission(self, request):
        return super().has_add_permission(request) and settings.DEBUG

    def has_delete_permission(self, request, obj=None):
        return super().has_add_permission(request) and settings.DEBUG

    @transaction.atomic
    def change_balance(self, request, queryset, amount):
        for user in queryset:
            user.balance = F("balance") + amount
            user.save()

            content_type = ContentType.objects.get_for_model(user)

            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=content_type.pk,
                object_id=user.pk,
                object_repr=repr(user),
                action_flag=CHANGE,
                change_message=f"Change Balance ({amount:+})",
            )

    def deposit(self, request, queryset):
        amount = int(request.POST["amount"])
        self.change_balance(request, queryset, amount)

    def withdraw(self, request, queryset):
        amount = int(request.POST["amount"])
        amount *= -1
        self.change_balance(request, queryset, amount)
