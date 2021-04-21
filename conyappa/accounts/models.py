from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models, transaction
from django.db.models import F

from lottery.models import Draw, get_number_of_tickets
from main.base import BaseModel, ExtendedQ


def generate_initial_extra_tickets_ttl():
    return settings.INITIAL_EXTRA_TICKETS_TTL


class UserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def everything(self):
        return super().get_queryset()

    @transaction.atomic
    def create(self, **fields):
        password = fields.pop("password", None)
        user = super().create(**fields)

        if password is not None:
            user.set_password(password)
            user.save()

        return user

    def create_superuser(self, **fields):
        fields.setdefault("is_staff", True)
        fields.setdefault("is_superuser", True)

        return self.create_user(**fields)


class User(BaseModel, AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    username = None
    email = models.EmailField(unique=True, null=True, max_length=254, verbose_name="email address")
    password = models.CharField(null=True, max_length=128, verbose_name="password")

    rut = models.PositiveIntegerField(unique=True, null=True, default=None, verbose_name="RUT")
    check_digit = models.PositiveSmallIntegerField(null=True, default=None, verbose_name="RUT check digit")

    balance = models.PositiveIntegerField(default=0, verbose_name="balance")
    winnings = models.PositiveIntegerField(default=0, verbose_name="winnings")

    extra_tickets_ttl = ArrayField(
        base_field=models.PositiveSmallIntegerField(),
        blank=True,
        default=generate_initial_extra_tickets_ttl,
        verbose_name="extra tickets TTL",
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

    @property
    def current_tickets(self):
        # This method assumes there is an ongoing draw.
        return self.tickets.ongoing()

    @property
    def current_prize(self):
        return sum(map(lambda x: x.prize, self.current_tickets))

    @property
    def owners(self):
        return {self}

    #####################
    # NUMBER OF TICKETS #
    #####################

    @property
    def number_of_standard_tickets(self):
        return get_number_of_tickets(self.balance)

    @property
    def number_of_extra_tickets(self):
        self.extra_tickets_ttl = [x for x in self.extra_tickets_ttl if (x > 0)]
        self.save()
        return len(self.extra_tickets_ttl)

    @property
    def number_of_tickets(self):
        return self.number_of_standard_tickets + self.number_of_extra_tickets

    @property
    def current_number_of_tickets(self):
        return self.current_tickets.count()

    ##############
    # OPERATIONS #
    ##############

    @transaction.atomic
    def deposit(self, amount):
        self.balance = F("balance") + amount
        self.save()

        draw = Draw.objects.ongoing()
        delta_tickets = get_number_of_tickets(amount)
        draw.add_tickets(user=self, n=delta_tickets)

    @transaction.atomic
    def withdraw(self, amount):
        # Avoid race conditions by locking the tickets until the end of the transaction.
        # This means that the selected tickets will only be modified (or deleted)
        # by a single instance of the back end at a time.
        # The transaction will proceed unless these tickets were already locked by another instance.
        # In that case, the transaction will block until they are released.
        locked_tickets = self.current_tickets.select_for_update()

        self.balance = F("balance") - amount
        self.save()

        ordered_tickets = locked_tickets.order_by("number_of_matches")
        delta_tickets = get_number_of_tickets(amount)
        pks_to_remove = ordered_tickets[:delta_tickets].values_list("pk")

        tickets_to_remove = locked_tickets.filter(pk__in=pks_to_remove)
        tickets_to_remove.delete()

    def consume_extra_tickets(self):
        self.extra_tickets_ttl = [(x - 1) for x in self.extra_tickets_ttl]
        self.save()

    def award_prize(self, value):
        self.balance = F("balance") + value
        self.winnings = F("winnings") + value
        self.save()

    #####################
    # LAZY REGISTRATION #
    #####################

    @property
    def is_registered(self):
        return bool(self.email) or bool(self.rut)

    @property
    def is_abandoned(self):
        return self.devices.count() == 0

    @property
    def is_null(self):
        return (not self.is_registered) and self.is_abandoned

    ###################
    # REPRESENTATIONS #
    ###################

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

    def __str__(self):
        return self.email if self.is_registered else "<anonymous>"


class Device(BaseModel):
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=ExtendedQ(android_id__isnull=False) ^ ExtendedQ(ios_id__isnull=False),
                name="exactly_one_os_id",
            )
        ]

    user = models.ForeignKey(
        to="accounts.User", null=True, verbose_name="user", related_name="devices", on_delete=models.SET_NULL
    )

    android_id = models.CharField(unique=True, null=True, max_length=255, verbose_name="Android ID")
    ios_id = models.CharField(unique=True, null=True, max_length=255, verbose_name="iOS ID")

    expo_push_token = models.CharField(unique=True, null=True, max_length=255, verbose_name="Expo push token")

    @property
    def os(self):
        return (self.android_id and "Android") or (self.ios_id and "iOS")

    @property
    def os_id(self):
        return self.android_id or self.ios_id

    def __str__(self):
        return f"{self.user or 'No one'}’s {self.os}"
