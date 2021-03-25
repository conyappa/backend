from django.db import models

from main.base import BaseModel


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

    @property
    def amount(self):
        return self.fintoc_data.get("amount")

    @property
    def raw_rut(self):
        sender_account = self.fintoc_data.get("sender_account") or {}
        return sender_account.get("holder_id")

    @property
    def rut(self):
        raw_rut = self.raw_rut
        return int(raw_rut[:-1]) if isinstance(raw_rut, str) else None

    @property
    def name(self):
        sender_account = self.fintoc_data.get("sender_account") or {}
        return sender_account.get("holder_name")

    def __str__(self):
        return f"{self.name} | ${self.amount}"
