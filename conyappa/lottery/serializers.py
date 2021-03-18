from rest_framework.serializers import ModelSerializer

from .models import Draw


class DrawSerializer(ModelSerializer):
    class Meta:
        model = Draw

        fields = [
            "results",
        ]

        extra_kwargs = {
            "results": {"read_only": True},
        }
