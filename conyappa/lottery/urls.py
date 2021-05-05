from django.urls import path

from .views import (
    DrawListView,
    LuckyTicketDetailView,
    OngoingDrawView,
    UserLuckyTicketsView,
    UserTicketsView,
    choose_result,
    draws_metadata,
)

app_name = "lottery"

urlpatterns = [
    path("draws", DrawListView.as_view(), name="draw-list"),
    path("draws/metadata", draws_metadata, name="draws-metadata"),
    path("draws/ongoing", OngoingDrawView.as_view(), name="ongoing-draw"),
    path("draws/ongoing/choose", choose_result, name="choose-result"),
    path("users/<uuid:user_id>/tickets", UserTicketsView.as_view(), name="user-tickets"),
    path("users/<uuid:user_id>/lucky-tickets", UserLuckyTicketsView.as_view(), name="user-lucky-tickets"),
    path("lucky-tickets/<uuid:pk>", LuckyTicketDetailView.as_view(), name="lucky-ticket-detail"),
]
