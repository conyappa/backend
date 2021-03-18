from django.urls import path

from .views import DrawListView

app_name = "lottery"

urlpatterns = [
    path("draws", DrawListView.as_view(), name="draw-list"),
]
