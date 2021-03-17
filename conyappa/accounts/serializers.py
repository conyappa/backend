from rest_framework.serializers import ModelSerializer

from .models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "rut",
            "check_digit",
            "formatted_rut",
            "balance",
            "winnings",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)
