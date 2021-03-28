from rest_framework.serializers import ListSerializer, ModelSerializer

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

        draw = Draw.objects.ongoing()
        results = draw.results
        picks_repr = lambda n: {"value": n, "in_results": n in results}

        return [{k: (map(picks_repr, v) if (k == "picks") else v) for (k, v) in rep.items()} for rep in reps]


class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        list_serializer_class = TicketListSerializer

        fields = [
            "number_of_matches",
            "prize",
            "picks",
        ]

        extra_kwargs = {
            # Choosing picks is a feature we would like to have in the near future.
            # For now, and for security reasons, make them read-only.
            "picks": {"read_only": True},
        }
