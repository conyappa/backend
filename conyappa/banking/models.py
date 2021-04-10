from django.db import models, transaction

from main.base import BaseModel

from logging import getLogger
logger = getLogger(__name__)


class Movement(BaseModel):
    class Meta:
        ordering = ["-fintoc_post_date"]
        indexes = [models.Index(fields=["fintoc_id"])]

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

    def set_original_values(self):
        self.__original_user = self.user
        self.__original_amount = self.amount

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_original_values()

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.user != self.__original_user:
            self.user.deposit(self.amount)

            if self.__original_user is not None:
                self.__original_user.withdraw(self.__original_amount)

        elif self.amount != self.__original_amount:
            self.user.withdraw(self.__original_amount)
            self.user.deposit(self.amount)

        super().save(*args, **kwargs)
        self.set_original_values()

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
