from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import CharField, ChoiceField, ModelForm, TextInput

import cron_descriptor
from .models import Rule


class RuleForm(ModelForm):
    class Meta:
        model = Rule
        fields = ["name", "function", "schedule_expression"]

    FUNCTION_CHOICES = [
        ("CREATE_DRAW", "Create draw"),
    ]

    SCHEDULE_EXPRESSION_EXAMPLES = [
        "cron(0/5 * * * * *)",
        "cron(0 20 * * * *)",
        "rate(5 minutes)",
        "cron(0 * 2 3 * *)",
        "cron(0 */10 * * * *)",
    ]

    function = ChoiceField(choices=FUNCTION_CHOICES, required=True)

    schedule_expression = CharField(
        required=True,
        widget=TextInput(attrs={"placeholder": SCHEDULE_EXPRESSION_EXAMPLES[0]}),
        help_text=(
            "AWS supports cron expressions and rate expressions."
            "\nAll scheduled events use UTC time zone and the minimum precision for schedules is 1 minute."
            f"\nExamples: {', '.join(SCHEDULE_EXPRESSION_EXAMPLES[1:])}."
        ),
    )

    @property
    def parsed_schedule_expression(self):
        EXPRESSION_TYPES = "cron", "rate"
        schedule_expression = self.cleaned_data["schedule_expression"]

        for type_ in EXPRESSION_TYPES:
            if schedule_expression.startswith(type_):
                expression = schedule_expression.lstrip(f"{type_}(").rstrip(")")
                return type_, expression

        raise ValidationError("Enter cron or rate expressions only.")

    @staticmethod
    def validate_cron(expression):
        try:
            cron_descriptor.get_description(expression)
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
        type_, expression = self.parsed_schedule_expression

        validators = {"cron": self.validate_cron, "rate": self.validate_rate}
        validators[type_](expression)

        return type_, expression


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

    form = RuleForm
