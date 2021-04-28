import datetime as dt

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models, transaction
from django.db.models import Count, F, Func
from django.db.models.functions import Cast

from main.base import BaseModel
from utils import random, sql
from utils.query import RelatedQuerySetMixin


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
            user_tickets = draw.generate_tickets(user=user, n=user.number_of_tickets)
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

    def generate_tickets(self, user, n):
        return [Ticket(draw=self, user=user, picks=generate_random_picks(pool=self.pool)) for _ in range(n)]

    def add_tickets(self, user, n):
        random.update()

        tickets = self.generate_tickets(user=user, n=n)
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
        for user in self.users.all():
            tickets = user.current_tickets
            prize = tickets.prize()
            user.award_prize(prize)

    def __str__(self):
        return str(self.start_date)


class TicketQuerySet(RelatedQuerySetMixin, models.QuerySet):
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

        return self.annotate(number_of_matches=Cast(function_call, output_field=models.IntegerField()))

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

    def prize(self):
        """
        Computes the prize of many tickets in an aggregated way, which, at a large scale,
        is much more efficient than the naive way: sum(ticket.prize for ticket in self).
        """

        is_related_to_draw = self.is_related_to_instance and isinstance(self.instance, Draw)

        if not is_related_to_draw:
            raise AttributeError("Ensure the QuerySet is related to a Draw.")

        draw = self.instance
        total_drilled_down_count = draw.tickets.all().drilled_down_count()

        base_prize = lambda number_of_matches, count: settings.PRIZES[number_of_matches] * count

        denominator = (
            lambda number_of_matches: total_drilled_down_count[number_of_matches]
            if (settings.PRIZE_IS_SHARED[number_of_matches] and total_drilled_down_count[number_of_matches])
            else 1
        )

        return sum(map(lambda el: base_prize(el[0], el[1]) / denominator(el[0]), self.drilled_down_count().items()))


class TicketManager(models.Manager):
    def get_queryset(self):
        qs_extra_kwargs = {}

        if hasattr(self, "instance"):
            qs_extra_kwargs["instance"] = self.instance

        qs = TicketQuerySet(self.model, using=self._db, **qs_extra_kwargs)
        return qs.annotate_matches().annotate_number_of_matches()

    def ongoing(self):
        draw = Draw.objects.ongoing()
        return draw.tickets.filter(pk__in=self.values_list("pk"))


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

    @property
    def prize(self):
        number_of_matches = self.number_of_matches
        value = settings.PRIZES[number_of_matches]

        if settings.PRIZE_IS_SHARED[number_of_matches]:
            tickets = self.draw.tickets
            tickets_with_same_number_of_matches = tickets.filter(number_of_matches=number_of_matches)
            value /= tickets_with_same_number_of_matches.count()

        return value

    def __str__(self):
        return str(self.picks)
