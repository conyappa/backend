import datetime as dt
from random import SystemRandom

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models, transaction

from main.base import BaseModel

WEEKDAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


# Alternative random generator that uses os.urandom (therefore, it’s better).
rd = SystemRandom()


def generate_random_picks():
    return rd.sample(population=Draw.objects.ongoing().pool, k=7)


def generate_result_pool():
    return list(settings.PICK_RANGE)


class DrawManager(models.Manager):
    def ongoing(self):
        # This method assumes that there is an ongoing draw.
        return self.latest("created_at")

    @transaction.atomic
    def create(self, **fields):
        User = get_user_model()
        users = User.objects.all()

        today = dt.date.today()
        fields.setdefault("start_date", today)

        draw = super().create(**fields)
        tickets = []

        for user in users:
            user_tickets = draw.generate_user_tickets(user=user)
            tickets += user_tickets
            user.consume_extra_tickets()

        Ticket.objects.bulk_create(objs=tickets)
        return draw


class Draw(BaseModel):
    class Meta:
        ordering = ["-created_at"]

    start_date = models.DateField(verbose_name="start date")
    pool = models.JSONField(default=generate_result_pool, verbose_name="result pool")
    results = models.JSONField(blank=True, default=list, verbose_name="results")

    objects = DrawManager()

    def generate_user_tickets(self, user):
        return [Ticket(draw=self, user=user) for _ in range(user.number_of_tickets)]

    def include_new_user(self, user):
        user_tickets = self.generate_user_tickets(user=user)
        Ticket.objects.bulk_create(objs=user_tickets)

    def choose_result(self):
        results = rd.sample(population=self.pool, k=1)

        # Eventual race conditions are not avoided by the following code.
        # Note that F expressions are not compatible with JSONField.
        self.pool = list(set(self.pool) - set(results))
        self.results += results
        self.save()

    @transaction.atomic
    def conclude(self):
        result_set = set(self.results)
        for ticket in self.tickets.all():
            number_of_matches = len(result_set & set(ticket.picks))
            user = ticket.user
            value = settings.PRIZES[number_of_matches]
            user.award_prize(value)

    def __str__(self):
        return str(self.start_date)


class TicketManager(models.Manager):
    def ongoing(self):
        current_draw = Draw.objects.ongoing()
        return self.filter(draw=current_draw)


class Ticket(BaseModel):
    picks = models.JSONField(default=generate_random_picks)
    draw = models.ForeignKey(
        to="lottery.Draw",
        verbose_name="draw",
        related_name="tickets",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        to="accounts.User",
        verbose_name="user",
        related_name="tickets",
        on_delete=models.CASCADE,
    )

    objects = TicketManager()

    @property
    def number_of_matches(self):
        result_set = set(self.draw.results)
        return len(result_set & set(self.picks))

    @property
    def prize(self):
        return settings.PRIZES[self.number_of_matches]
