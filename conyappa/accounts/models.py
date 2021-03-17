from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction

from main.base import BaseModel


def generate_initial_extra_tickets_ttl():
    return settings.INITIAL_EXTRA_TICKETS_TTL


class UserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def everything(self):
        return super().get_queryset()

    @transaction.atomic
    def create_user(self, **fields):
        password = fields.pop("password", None)
        user = self.create(**fields)

        if password is not None:
            user.set_password(password)
            user.save()

        return user

    def create_superuser(self, **fields):
        fields.setdefault("is_staff", True)
        fields.setdefault("is_superuser", True)

        return self.create_user(**fields)


class User(BaseModel, AbstractUser):
    class Meta:
        indexes = [models.Index(fields=["rut"])]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    username = None
    email = models.EmailField(unique=True, max_length=254, verbose_name="email address")

    rut = models.PositiveIntegerField(unique=True, null=True, default=None, verbose_name="RUT")
    check_digit = models.PositiveSmallIntegerField(null=True, default=None, verbose_name="RUT check digit")

    balance = models.PositiveIntegerField(default=0, verbose_name="balance")
    winnings = models.PositiveIntegerField(default=0, verbose_name="winnings")
    extra_tickets_ttl = models.JSONField(
        blank=True, default=generate_initial_extra_tickets_ttl, verbose_name="extra tickets TTL"
    )

    objects = UserManager()

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save(*args, **kwargs)

    def restore(self, *args, **kwargs):
        self.is_active = True
        self.save(*args, **kwargs)

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def consume_extra_tickets(self):
        self.extra_tickets_ttl = [(x - 1) for x in self.extra_tickets_ttl]
        self.save()

    def award_prize(self, value):
        self.balance += value
        self.winnings += value
        self.save()

    @property
    def number_of_standard_tickets(self):
        return min(settings.MAX_TICKETS, self.balance // settings.TICKET_COST)

    @property
    def number_of_extra_tickets(self):
        self.extra_tickets_ttl = [x for x in self.extra_tickets_ttl if (x > 0)]
        self.save()
        return len(self.extra_tickets_ttl)

    @property
    def number_of_tickets(self):
        return self.number_of_standard_tickets + self.number_of_extra_tickets

    @property
    def current_tickets(self):
        # This method assumes there is an ongoing draw.
        return self.tickets.ongoing()

    @property
    def number_of_current_tickets(self):
        return self.current_tickets.count()

    @property
    def current_prize(self):
        return sum(map(lambda x: x.prize, self.current_tickets))

    @property
    def full_name(self):
        name_components = filter(bool, [self.first_name, self.last_name])
        name = " ".join(name_components)
        return name

    @property
    def formatted_rut(self):
        if (self.rut is None) or (self.check_digit is None):
            return

        rut_w_thousands_sep = "{:,}".format(self.rut).replace(",", ".")
        formatted_check_digit = "K" if (self.check_digit == 10) else self.check_digit
        return f"{rut_w_thousands_sep}-{formatted_check_digit}"

    @property
    def owners(self):
        return {self}

    def __str__(self):
        return self.email
