from django.urls import path

from rest_framework_simplejwt.views import TokenObtainSlidingView

app_name = "accounts"

urlpatterns = [
    path("login/", TokenObtainSlidingView.as_view(), name="login"),
]
