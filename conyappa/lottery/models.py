import datetime as dt
import math

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models, transaction
from django.db.models import Count, F, Func

from main.base import BaseModel
from utils import random, sql


def generate_result_pool():
    return list(settings.PICK_RANGE)


def generate_random_picks(pool):
    rd = random.get()
    return rd.sample(population=pool, k=7)


def get_number_of_tickets(balance):
    return balance // settings.TICKET_COST


class DrawManager(models.Manager):
    def ongoing(self):
        # This method assumes that there is an ongoing draw.
        return self.latest("created_at")

    @transaction.atomic
    def create(self, **fields):
        random.update()

        User = get_user_model()
        users = User.objects.all()

        today = dt.date.today()
        fields.setdefault("start_date", today)

        draw = super().create(**fields)
        tickets = []

        for user in users:
            n = user.number_of_tickets
            user_lucky_tickets = user.lucky_tickets.all()[:n]
            user_tickets = draw.generate_tickets_from_lucky_tickets(qs=user_lucky_tickets)

            n -= len(user_tickets)
            user_tickets += draw.generate_random_tickets(user=user, n=n)

            tickets += user_tickets
            user.consume_extra_tickets()

        Ticket.objects.bulk_create(objs=tickets)
        return draw


class Draw(BaseModel):
    class Meta:
        ordering = ["-created_at"]

    start_date = models.DateField(verbose_name="start date")

    pool = ArrayField(
        base_field=models.PositiveSmallIntegerField(), default=generate_result_pool, verbose_name="result pool"
    )
    results = ArrayField(
        base_field=models.PositiveSmallIntegerField(), blank=True, default=list, verbose_name="results"
    )

    objects = DrawManager()

    def generate_tickets_from_lucky_tickets(self, qs):
        return [Ticket(draw=self, user=lucky_ticket.user, picks=lucky_ticket.picks) for lucky_ticket in qs]

    def generate_random_tickets(self, user, n):
        return [Ticket(draw=self, user=user, picks=generate_random_picks(pool=self.pool)) for _ in range(n)]

    def add_random_tickets(self, user, n):
        random.update()

        tickets = self.generate_random_tickets(user=user, n=n)
        Ticket.objects.bulk_create(objs=tickets)

    def choose_result(self):
        random.update()
        rd = random.get()

        results = rd.sample(population=self.pool, k=1)

        # Eventual race conditions are not avoided by the following code.
        # Note that F expressions are not compatible with JSONField.
        # Anyway, this method should be called only once a day.
        self.pool = list(set(self.pool) - set(results))
        self.results += results
        self.save()

    @transaction.atomic
    def conclude(self):
        User = get_user_model()
        drilled_down_count = self.tickets.all().drilled_down_count()

        for user in User.objects.all():
            tickets = user.tickets.filter(draw=self)
            prize_after_sharing = tickets.prize(total_drilled_down_count=drilled_down_count)
            user.award_prize(prize_after_sharing)

    def __str__(self):
        return str(self.start_date)


class TicketQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create the custom array_intersect SQL function.
        function_creation = sql.loads("create_array_intersect")
        sql.execute(function_creation)

    def annotate_matches(self):
        expressions = [F("picks"), F("draw__results")]
        function_call = Func(*expressions, function="array_intersect", arity=2)

        return self.annotate(matches=function_call)

    def annotate_number_of_matches(self):
        expressions = [F("matches")]
        function_call = Func(*expressions, function="cardinality", arity=1)

        return self.annotate(number_of_matches=function_call)

    def drilled_down_count(self):
        """
        Returns a dictionary with the ticket count per number of matches.
        """
        ticket_count = {i: 0 for i in range(8)}
        number_of_matches = self.values("number_of_matches")

        ticket_count.update(
            {el["number_of_matches"]: el["count"] for el in number_of_matches.annotate(count=Count("pk"))}
        )

        return ticket_count

    def prize(self, total_drilled_down_count=None):
        """
        Computes the prize of many tickets in an aggregated way, which, at a large scale,
        is much more efficient than the naive way: computing the prize of each ticket and then adding the results.
        """

        def base_prize(number_of_matches, count):
            prize = settings.PRIZES[number_of_matches]
            return count * prize

        def denominator(number_of_matches):
            is_shared_prize = settings.IS_SHARED_PRIZE[number_of_matches]
            total_count = total_drilled_down_count and total_drilled_down_count[number_of_matches]

            return (is_shared_prize and total_count) or 1

        value = sum(
            (base_prize(number_of_matches, count) / denominator(number_of_matches))
            for (number_of_matches, count) in self.drilled_down_count().items()
        )

        return math.ceil(value)


class TicketManager(models.Manager):
    def get_queryset(self):
        qs = TicketQuerySet(self.model, using=self._db)
        return qs.annotate_matches().annotate_number_of_matches()

    def ongoing(self):
        draw = Draw.objects.ongoing()
        return self.filter(draw=draw)


class Ticket(BaseModel):
    picks = ArrayField(base_field=models.PositiveSmallIntegerField(), null=True)

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

    def __str__(self):
        return str(self.picks)


class LuckyTicket(BaseModel):
    class Meta:
        ordering = ["created_at"]

    picks = ArrayField(base_field=models.PositiveSmallIntegerField())

    user = models.ForeignKey(
        to="accounts.User",
        verbose_name="user",
        related_name="lucky_tickets",
        on_delete=models.CASCADE,
    )

    @property
    def owners(self):
        return {self.user}

    def __str__(self):
        return str(self.picks)
