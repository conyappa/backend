from django.urls import path

from .views import fetch_movements

app_name = "lottery"

urlpatterns = [
    path("movements/fetch", fetch_movements, name="fetch-movements"),
]
