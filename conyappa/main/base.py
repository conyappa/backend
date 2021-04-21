import uuid

from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        serialize=False,
        unique=True,
        verbose_name="ID",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="last updated at")


class ExtendedQ(models.Q):
    def __xor__(self, other):
        neg_self = ~self
        neg_other = ~other
        return (self & neg_other) | (neg_self & other)
