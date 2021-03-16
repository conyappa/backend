from django.urls import include, path

from . import views

urlpatterns = [
    path("admin", views.admin_site.urls),
    path("error", views.trigger_error),
    path("v1/", include("accounts.urls")),
]
