from django import db
from django.contrib.admin import site as admin_site
from django.db.utils import OperationalError

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE

admin_site.site_header = "Con Yappa"
admin_site.site_title = "Con Yappa"


@api_view(["GET"])
def health_check(request):
    db_conn = db.connections["default"]
    try:
        db_conn.cursor()
    except OperationalError:
        return Response(data={"detail": "Can't connect to database."}, status=HTTP_503_SERVICE_UNAVAILABLE)
    except Exception:
        return Response(
            data={"detail": "Unknown database problem."},
            status=HTTP_503_SERVICE_UNAVAILABLE,
        )
    return Response(status=HTTP_200_OK)


@api_view(["GET"])
def trigger_error(_request):
    raise Exception("This is just a test.")
