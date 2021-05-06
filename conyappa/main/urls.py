from django.urls import include, path, re_path

from .versioning import ALLOWED_VERSIONS
from .views import admin_site, health_check, trigger_error

allowed_versions_string = "|".join(ALLOWED_VERSIONS)

urlpatterns = [
    path("admin", admin_site.urls),
    path("", include("docs.urls")),
    re_path(
        rf"(?P<version>({allowed_versions_string}))/",
        include(
            [
                path("", include("accounts.urls")),
                path("", include("banking.urls")),
                path("", include("lottery.urls")),
            ]
        ),
    ),
    path("", health_check),
    path("error", trigger_error),
]
