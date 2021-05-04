from collections import OrderedDict

from django.utils.functional import cached_property

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class TicketPaginator(PageNumberPagination.django_paginator_class):
    @cached_property
    def total_prize(self):
        return self.object_list.prize()


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
