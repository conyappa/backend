from django.conf import settings

from rest_framework.serializers import (
    BooleanField,
    IntegerField,
    JSONField,
    ListSerializer,
    ModelSerializer,
    Field
)

from .models import Draw, Ticket


class DrawSerializer(ModelSerializer):
    class Meta:
        model = Draw

        fields = [
            "start_date",
            "results",
        ]

        extra_kwargs = {
            "start_date": {"read_only": True},
            "results": {"read_only": True},
        }


class TicketPicksField(Field):
    def get_attribute(self, instance):
        return instance

    def to_representation(self, value):
        sorted_picks = sorted(value.picks)
        return [{"value": pick, "in_results": (pick in value.matches)} for pick in sorted_picks]


class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket

        fields = [
            "number_of_matches",
            "prize",
            "is_shared_prize",
            "picks",
        ]

        extra_kwargs = {
            # Choosing picks is a feature we would like to have in the near future.
            # For now, and for security reasons, make them read-only.
            "picks": {"read_only": True},
        }

    number_of_matches = IntegerField(read_only=True)
    picks = TicketPicksField(read_only=True)
