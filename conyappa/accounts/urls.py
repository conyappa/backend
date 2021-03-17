from django.urls import path

from .views import TokenLoginView, UserListView

app_name = "accounts"

urlpatterns = [
    path("login/", TokenLoginView.as_view(), name="login"),
    path("users/", UserListView.as_view(), name="user-list"),
]
