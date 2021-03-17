from django.urls import path

from .views import TokenLoginView

app_name = "accounts"

urlpatterns = [
    path("login/", TokenLoginView.as_view(), name="login"),
]
