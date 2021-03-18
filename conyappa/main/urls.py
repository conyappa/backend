from django.urls import include, path

from .views import admin_site, health_check, trigger_error

urlpatterns = [
    path("admin", admin_site.urls),
    path(
        "v1/",
        include(
            [
                path("health-check", health_check),
                path("error", trigger_error),
                path("docs/", include("docs.urls")),
                path("", include("accounts.urls")),
                path("", include("lottery.urls")),
            ]
        ),
    ),
]
