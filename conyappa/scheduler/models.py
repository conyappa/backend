from django.db import models, transaction

from main.base import BaseModel

from . import eventbridge
from .utils import SCHEDULE_DESCRIPTORS, parse_schedule


class RuleQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.delete()


class RuleManager(models.Manager):
    def get_queryset(self):
        return RuleQuerySet(self.model, using=self._db)


class Rule(BaseModel):
    name = models.CharField(unique=True, max_length=50, verbose_name="Name")

    objects = RuleManager()

    def init_remote(self, **kwargs):
        eventbridge.Interface().fetch(self)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.name:
            self.init_remote()

    def save_remote(self):
        eventbridge.Interface().put(self)

    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.save_remote()

    def delete_remote(self):
        eventbridge.Interface().delete(self)

    @transaction.atomic
    def delete(self, *args, **kwargs):
        pk = self.pk
        super().delete(*args, **kwargs)
        self.pk = pk
        self.delete_remote()

    @property
    def unique_name(self):
        return f"{self.name}_{self.pk}"

    @property
    def schedule(self):
        type_, expression = parse_schedule(self.schedule_expression)

        description = SCHEDULE_DESCRIPTORS[type_](expression)
        return f"{self.schedule_expression} => {description}"

    def __str__(self):
        return self.name
