from django.contrib import admin
from django.forms import CharField, ChoiceField, ModelForm, TextInput

from .models import Rule


class RuleForm(ModelForm):
    class Meta:
        model = Rule
        fields = ["name", "schedule_expression", "function"]

    function_choices = [
        ("CREATE_DRAW", "Create draw"),
    ]

    function = ChoiceField(choices=function_choices)

    schedule_expression = CharField(
        widget=TextInput(attrs={"placeholder": "cron(0/5 * * * * *)"}),
        help_text=(
            "AWS supports cron expressions and rate expressions."
            "\nAll scheduled events use UTC time zone and the minimum precision for schedules is 1 minute."
            "\nExamples: cron(0 20 * * ? *), rate(5 minutes), cron(0 * 2 3 * *), cron(*/10 * * * *)."
        ),
    )


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
