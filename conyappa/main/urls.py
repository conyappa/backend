from django.urls import path

from . import views

urlpatterns = [
    path("admin", views.admin_site.urls),
    path("exception", views.trigger_exception),
]
