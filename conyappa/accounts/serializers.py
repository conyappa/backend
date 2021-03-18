from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainSlidingSerializer

from .models import User


class TokenLoginSerializer(TokenObtainSlidingSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["id"] = self.user.id
        return data


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
            "password",
            "balance",
            "winnings",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
            "balance": {"read_only": True},
            "winnings": {"read_only": True},
        }
