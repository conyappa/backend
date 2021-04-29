from django.conf import settings

from rest_framework.serializers import (
    BooleanField,
    IntegerField,
    JSONField,
    ListSerializer,
    ModelSerializer,
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


class TicketListSerializer(ListSerializer):
    def to_representation(self, data):
        reps = super().to_representation(data)

        def transform(rep):
            sorted_picks = sorted(rep["picks"])

            return {
                "number_of_matches": rep["number_of_matches"],
                "prize": rep["prize"],
                "is_shared_prize": settings.IS_SHARED_PRIZE[rep["number_of_matches"]],
                "picks": [{"value": pick, "in_results": pick in rep["matches"]} for pick in sorted_picks],
            }

        return list(map(transform, reps))


class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        list_serializer_class = TicketListSerializer

        fields = [
            "matches",
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

    matches = JSONField(read_only=True)
    number_of_matches = IntegerField(read_only=True)
    is_shared_prize = BooleanField(read_only=True)
