from rest_framework.serializers import JSONField, ListSerializer, ModelSerializer

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
            matches = rep["matches"]
            sorted_picks = sorted(rep["picks"])

            return {
                "number_of_matches": rep["number_of_matches"],
                "prize": rep["prize"],
                "picks": [{"value": pick, "in_results": pick in matches} for pick in sorted_picks],
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
            "picks",
        ]

        extra_kwargs = {
            # Choosing picks is a feature we would like to have in the near future.
            # For now, and for security reasons, make them read-only.
            "picks": {"read_only": True},
        }

    matches = JSONField()
