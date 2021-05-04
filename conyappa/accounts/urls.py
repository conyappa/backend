from django.urls import path

from .views import (
    RefreshTokenView,
    TokenLoginView,
    UserDetailView,
    UserDeviceListView,
    UserListView,
)

app_name = "accounts"

urlpatterns = [
    path("login", TokenLoginView.as_view(), name="legacy-login"),  # LEGACY
    path("auth/login", TokenLoginView.as_view(), name="login"),
    path("auth/refresh", RefreshTokenView.as_view(), name="refresh_token"),
    path("users", UserListView.as_view(), name="user-list"),
    path("users/<uuid:pk>", UserDetailView.as_view(), name="user-detail"),
    path("users/<uuid:user_id>/devices", UserDeviceListView.as_view(), name="user-device-list"),
]
