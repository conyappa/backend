from rest_framework.versioning import URLPathVersioning

ALLOWED_VERSIONS = ["v1", "v2"]


class VersioningClass(URLPathVersioning):
    default_version = "v2"
    allowed_versions = ALLOWED_VERSIONS


class VersioningMixin:
    versioning_class = VersioningClass
