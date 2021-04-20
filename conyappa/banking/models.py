from logging import getLogger

from django.contrib.auth import get_user_model
from django.db import models, transaction

from main.base import BaseModel

logger = getLogger(__name__)


class Movement(BaseModel):
    class Meta:
        ordering = ["-fintoc_post_date"]

    fintoc_data = models.JSONField(verbose_name="Fintoc object")
    fintoc_id = models.CharField(unique=True, verbose_name="Fintoc ID", max_length=32)
    fintoc_post_date = models.DateField(verbose_name="Fintoc post date")

    user = models.ForeignKey(
        to="accounts.User",
        null=True,
        default=None,
        verbose_name="user",
        related_name="movements",
        on_delete=models.PROTECT,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_user = self.user

    def lookup_associated_user(self):
        User = get_user_model()

        try:
            return User.objects.get(rut=self.rut)

        except (User.DoesNotExist, User.MultipleObjectsReturned) as e:
            logger.warning(f"Couldn’t associate movement to user: {e}")

    @transaction.atomic
    def save(self, *args, **kwargs):
        if (not self.__original_user) and (not self.user):
            # There is no information about the associated user,
            # so we must try to find one that matches the movement.
            self.user = self.lookup_associated_user()

        # Now we must check which action to perform.

        if self.__original_user and (not self.user):
            # The associated user is being removed.
            self.__original_user.withdraw(self.amount)

        elif (not self.__original_user) and self.user:
            # The associated user is being added.
            self.user.deposit(self.amount)

        elif self.__original_user != self.user:
            # The associated user is being corrected (changed).
            self.__original_user.withdraw(self.amount)
            self.user.deposit(self.amount)

        super().save(*args, **kwargs)
        self.__original_user = self.user

    @property
    def amount(self):
        fintoc_data = self.fintoc_data or {}
        return fintoc_data.get("amount")

    @property
    def raw_rut(self):
        fintoc_data = self.fintoc_data or {}
        sender_account = fintoc_data.get("sender_account") or {}
        return sender_account.get("holder_id")

    @property
    def rut(self):
        raw_rut = self.raw_rut
        return int(raw_rut[:-1]) if isinstance(raw_rut, str) else None

    @property
    def name(self):
        fintoc_data = self.fintoc_data or {}
        sender_account = fintoc_data.get("sender_account") or {}
        return sender_account.get("holder_name")

    def __str__(self):
        return f"{self.name} | ${self.amount}"
