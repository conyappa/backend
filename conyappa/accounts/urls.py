from django.urls import path

from rest_framework_simplejwt import views as jwt_views

app_name = "accounts"


urlpatterns = [
    path("login/", jwt_views.TokenObtainSlidingView.as_view(), name="login"),
]
