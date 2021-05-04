from django.conf import settings

from rest_framework.serializers import Field, IntegerField, ModelSerializer

from .models import Draw, Ticket


class PrizeField(Field):
    def to_representation(self, value):
        return {
            "value": settings.PRIZES[value],
            "is_shared": settings.IS_SHARED_PRIZE[value],
        }


class PrizeFieldVersion1(PrizeField):
    def to_representation(self, value):
        return settings.PRIZES[value]


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


class TicketPrizeField(PrizeField):
    def get_attribute(self, instance):
        return instance.number_of_matches


class TicketPrizeFieldVersion1(TicketPrizeField):
    def get_attribute(self, instance):
        return instance.number_of_matches


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
            "picks",
        ]

        extra_kwargs = {
            # Choosing picks is a feature we would like to have in the near future.
            # For now, and for security reasons, make them read-only.
            "picks": {"read_only": True},
        }

    number_of_matches = IntegerField(read_only=True)
    prize = TicketPrizeField(read_only=True)
    picks = TicketPicksField(read_only=True)


class TicketSerializerVersion1(TicketSerializer):
    prize = TicketPrizeFieldVersion1(read_only=True)
