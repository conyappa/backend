from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import TokenLoginView, UserDetailView, UserDeviceListView, UserListView

app_name = "accounts"

urlpatterns = [
    path("login", TokenLoginView.as_view(), name="legacy-auth-token"),  # LEGACY
    path("auth/login", TokenLoginView.as_view(), name="auth-token"),
    path("auth/refresh", TokenRefreshView.as_view(), name="refresh-token"),
    path("users", UserListView.as_view(), name="user-list"),
    path("users/<uuid:pk>", UserDetailView.as_view(), name="user-detail"),
    path("users/<uuid:user_id>/devices", UserDeviceListView.as_view(), name="user-device-list"),
]
