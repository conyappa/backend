from logging import getLogger

from django.db import models, transaction

from main.base import BaseModel

logger = getLogger(__name__)


class RuleQuerySet(models.QuerySet):
    def delete_remote(self):
        for obj in self:
            obj.delete_remote()

    @transaction.atomic
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.delete_remote()


class RuleManager(models.Manager):
    def get_queryset(self):
        return RuleQuerySet(self.model, using=self._db)


class Rule(BaseModel):
    name = models.CharField(unique=True, max_length=50, verbose_name="Name")

    objects = RuleManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save_remote(self):
        pass

    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.save_remote()

    def delete_remote(self):
        pass

    @transaction.atomic
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.delete_remote()
