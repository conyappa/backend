from django.urls import path

from rest_framework_simplejwt.views import TokenObtainSlidingView

from .views import UserListView

app_name = "accounts"

urlpatterns = [
    path("login/", TokenObtainSlidingView.as_view(), name="login"),
    path("users/", UserListView.as_view(), name="user-list"),
]
