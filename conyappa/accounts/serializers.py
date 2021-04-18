from rest_framework.serializers import ModelSerializer, ValidationError, CharField
from rest_framework_simplejwt.serializers import TokenObtainSlidingSerializer
from django.db import transaction
from utils.serializers import SetOnlyFieldsMixin

from .models import Device, User


class TokenLoginSerializer(TokenObtainSlidingSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["id"] = self.user.id
        return data


class UserSerializer(SetOnlyFieldsMixin, ModelSerializer):
    class Meta:
        model = User

        fields = [
            "id",
            "email",
            "rut",
            "check_digit",
            "formatted_rut",
            "password",
            "first_name",
            "last_name",
            "full_name",
            "balance",
            "winnings",
            "token",
        ]

        # These fields can only be set once.
        # I.e., they can only be changed if blank or null.
        set_only_fields = [
            "rut",
            "check_digit",
            "first_name",
            "last_name",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
            "balance": {"read_only": True},
            "winnings": {"read_only": True},
        }

    token = CharField(read_only=True, required=False)

    def create(self, validated_data):
        user = super().create(validated_data)
        user.token = TokenLoginSerializer.get_token(user)
        return user

    @transaction.atomic
    def save(self, **kwargs):
        user = super().save(**kwargs)

        if "password" in self.validated_data:
            password = self.validated_data["password"]
            user.set_password(password)
            user.save()

        return user

    @staticmethod
    def expected_check_digit(rut):
        remaining_digits = rut

        m = 0
        s = 1

        while remaining_digits > 0:
            last_digit = remaining_digits % 10
            remaining_digits //= 10

            coef = 9 - (m % 6)
            m += 1

            s += last_digit * coef
            s %= 11

        return (s - 1) if (s > 0) else 10

    def get_field_verbose_name(self, field_name):
        model = self.Meta.model
        return model._meta.get_field(field_name).verbose_name

    def validate_rut(self, value):
        check_digit_name = "check_digit"
        check_digit = self.initial_data.get(check_digit_name)
        check_digit_verbose_name = self.get_field_verbose_name(check_digit_name)

        if check_digit is None:
            raise ValidationError(f"Don't input this field without a {check_digit_verbose_name}.")

        return value

    def validate_check_digit(self, value):
        rut_name = "rut"
        rut = self.initial_data.get(rut_name)
        rut_verbose_name = self.get_field_verbose_name(rut_name)

        if rut is None:
            raise ValidationError(f"Don't input this field without a {rut_verbose_name}.")

        if value > 10:
            raise ValidationError("Ensure this value is less than or equal to 10.")

        if value != self.expected_check_digit(rut):
            raise ValidationError(f"Ensure this value corresponds to the inputted {rut_verbose_name}.")

        return value

    def validate_password(self, value):
        PASSWORD_MIN_LENGTH = 6

        if len(value) < PASSWORD_MIN_LENGTH:
            raise ValidationError(f"Ensure this field has no less than {PASSWORD_MIN_LENGTH} characters.")

        return value


class DeviceSerializer(ModelSerializer):
    class Meta:
        model = Device

        fields = [
            "user",
            "android_id",
            "ios_id",
            "expo_push_token",
        ]
