# from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSlidingSerializer


class TokenLoginSerializer(TokenObtainSlidingSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["id"] = self.user.id
        return data
