from rest_framework.serializers import ModelSerializer

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


class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket

        fields = [
            "picks",
        ]

        extra_kwargs = {
            # Choosing picks is a feature we would like to have in the near future.
            # For now, and for security reasons, make them read-only.
            "picks": {"read_only": True},
        }
