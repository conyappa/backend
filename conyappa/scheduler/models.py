from django.db import models, transaction

from main.base import BaseModel

from .eventbridge import Interface as EventBridge
from .utils import SCHEDULE_DESCRIPTORS, parse_schedule


class RuleQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        # Don’t use QuerySet deletion here;
        # each rule deletion must be atomic and independent.
        for obj in self:
            obj.delete()


class RuleManager(models.Manager):
    def get_queryset(self):
        return RuleQuerySet(self.model, using=self._db)


class Rule(BaseModel):
    name = models.CharField(unique=True, max_length=50, verbose_name="Name")

    objects = RuleManager()

    def init_remote(self, **kwargs):
        EventBridge().fetch(self)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_name = self.name

        if self.name:
            self.init_remote()

    def save_remote(self):
        EventBridge().put(self)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.__original_name and (self.name != self.__original_name):
            raise NotImplementedError("Please don’t to change the rule’s name.")

        super().save(*args, **kwargs)
        self.save_remote()

    def delete_remote(self):
        EventBridge().delete(self)

    @transaction.atomic
    def delete(self, *args, **kwargs):
        # Don’t lose the ID
        # because it’s used by eventbridge_name in delete_remote.
        pk = self.pk
        super().delete(*args, **kwargs)
        self.pk = pk
        self.delete_remote()

    @property
    def eventbridge_name(self):
        # Each rule name (and target ID) must be unique.
        return f"{self.name}_{self.pk}"

    @property
    def schedule(self):
        type_, expression = parse_schedule(self.schedule_expression)

        description = SCHEDULE_DESCRIPTORS[type_](expression)
        return f"{self.schedule_expression} => {description}"

    def __str__(self):
        return self.name
