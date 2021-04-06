from collections import OrderedDict
from functools import reduce
from logging import getLogger
from operator import add

from django.conf import settings
from django.db.models import Count, F
from django.utils.functional import cached_property

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

logger = getLogger(__name__)


class TicketPaginator(PageNumberPagination.django_paginator_class):
    @cached_property
    def total_prize(self):
        ticket_per_number_of_matches = self.object_list.values("number_of_matches").annotate(Count("id"))
        ticket_per_number_of_matches = ticket_per_number_of_matches.annotate(Count("id"))

        prizes = map(
            lambda el: settings.PRIZES[el["number_of_matches"]] * el["id__count"], ticket_per_number_of_matches
        )
        return sum(prizes)


class TicketPagination(PageNumberPagination):
    django_paginator_class = TicketPaginator

    page_size = 100
    max_page_size = 1000
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("total_prize", self.page.paginator.total_prize),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )
