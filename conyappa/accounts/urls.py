from django.urls import path

from .views import TokenLoginView, RefreshTokenView, UserDetailView, UserDeviceListView, UserListView

app_name = "accounts"

urlpatterns = [
    path("auth/login", TokenLoginView.as_view(), name="login"),
    path("auth/refresh", RefreshTokenView.as_view(), name="refresh_token"),
    path("users", UserListView.as_view(), name="user-list"),
    path("users/<uuid:pk>", UserDetailView.as_view(), name="user-detail"),
    path("users/<uuid:user_id>/devices", UserDeviceListView.as_view(), name="user-device-list"),
]
