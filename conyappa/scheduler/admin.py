from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import CharField, ChoiceField, ModelForm, TextInput

import cron_descriptor

from .models import Rule
from .utils import CRON, RATE, SCHEDULE_DESCRIPTORS, parse_schedule


class RuleForm(ModelForm):
    class Meta:
        model = Rule

        fields = [
            "name",
            "function",
            "schedule_expression",
        ]

    FUNCTION_CHOICES = [
        (settings.AWS_CREATE_DRAW_LAMBDA, "Create draw"),
    ]

    function = ChoiceField(choices=FUNCTION_CHOICES, required=True)

    SCHEDULE_EXPRESSION_EXAMPLES = [
        "cron(0/5 * * * ? *)",
        "cron(0 20 * * ? *)",
        "rate(5 minutes)",
        "cron(0 * 2 3 * *)",
        "cron(0 */10 * * * *)",
    ]

    schedule_expression = CharField(
        required=True,
        widget=TextInput(attrs={"placeholder": SCHEDULE_EXPRESSION_EXAMPLES[0]}),
        help_text=(
            "AWS supports cron expressions and rate expressions."
            "\nAll scheduled events use UTC time zone and the minimum precision for schedules is 1 minute."
            f"\nExamples: {', '.join(SCHEDULE_EXPRESSION_EXAMPLES[1:])}."
        ),
    )

    @staticmethod
    def validate_cron(expression):
        try:
            SCHEDULE_DESCRIPTORS[CRON](expression)
        except cron_descriptor.FormatException as e:
            raise ValidationError(f"Invalid cron expression: {e}")

    @staticmethod
    def validate_rate(expression):
        try:
            value, unit = expression.split(" ")
        except ValueError:
            raise ValidationError("Invalid rate expression: ensure the input contains exactly one value and one unit.")

        if not value.isdigit():
            raise ValidationError("Invalid rate expression: ensure the inputted value is a whole number.")

    def clean_schedule_expression(self):
        schedule_expression = self.cleaned_data["schedule_expression"]
        type_, expression = parse_schedule(schedule_expression)

        validators = {CRON: self.validate_cron, RATE: self.validate_rate}
        validators[type_](expression)

        return type_, expression


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
    ]

    list_display = [
        "name",
        "schedule",
        "updated_at",
    ]

    list_filter = [
        "updated_at",
    ]

    form = RuleForm

    readonly_fields = [
        "schedule",
    ]

    def save_model(self, request, obj, form, change):
        function = form.cleaned_data["function"]
        type_, expression = form.cleaned_data["schedule_expression"]

        obj.function = function
        obj.schedule_expression = f"{type_}({expression})"

        super().save_model(request, obj, form, change)
