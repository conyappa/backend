from django.core.exceptions import ValidationError

import cron_descriptor

CRON = "cron"
RATE = "rate"


CRON_DESCRIPTOR_OPTIONS = cron_descriptor.Options()
CRON_DESCRIPTOR_OPTIONS.day_of_week_start_index_zero = False


def parse_schedule(schedule_expression):
    for type_ in [CRON, RATE]:
        if schedule_expression.startswith(type_):
            expression = schedule_expression.lstrip(f"{type_}(").rstrip(")")
            return type_, expression

    raise ValidationError("Enter cron or rate expressions only.")


def get_cron_description(expression):
    normal_form = "0 " + expression.replace("?", "*")

    descriptor_options = cron_descriptor.Options()
    descriptor_options.day_of_week_start_index_zero = False

    return cron_descriptor.get_description(expression=normal_form, options=descriptor_options)


def get_rate_description(expression):
    return f"Every {expression}"


SCHEDULE_DESCRIPTORS = {CRON: get_cron_description, RATE: get_rate_description}
