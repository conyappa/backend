from django.urls import include, path

from . import views

urlpatterns = [
    path("admin", views.admin_site.urls),
    path(
        "v1/",
        include(
            [
                path("error", views.trigger_error),
                path("docs/", include("docs.urls")),
                path("", include("accounts.urls")),
                path("", include("lottery.urls")),
            ]
        ),
    ),
]
