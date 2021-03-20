from django.urls import include, path

from .views import admin_site, health_check, trigger_error

urlpatterns = [
    path("admin", admin_site.urls),
    path("", include("docs.urls")),
    path(
        "v1/",
        include(
            [
                path("", include("accounts.urls")),
                path("", include("lottery.urls")),
            ]
        ),
    ),
    path("", health_check),
    path("error", trigger_error),
]
