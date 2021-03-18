from django.urls import path

from .views import TokenLoginView, UserDetailView, UserListView

app_name = "accounts"

urlpatterns = [
    path("login", TokenLoginView.as_view(), name="login"),
    path("users", UserListView.as_view(), name="user-list"),
    path("users/<uuid:pk>", UserDetailView.as_view(), name="user-detail"),
]
