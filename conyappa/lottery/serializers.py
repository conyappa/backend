from rest_framework.serializers import ModelSerializer

from .models import Draw


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
