from django.urls import path

from .views import DrawListView, OngoingDrawView, OngoingUserTicketsView

app_name = "lottery"

urlpatterns = [
    path("draws", DrawListView.as_view(), name="draw-list"),
    path("draws/ongoing", OngoingDrawView.as_view(), name="ongoing-draw"),
    path("users/<uuid:user_id>/tickets", OngoingUserTicketsView.as_view(), name="user-tickets"),
]
