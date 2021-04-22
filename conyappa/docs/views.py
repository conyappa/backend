import json
import os

from django.conf import settings
from django.shortcuts import render

from .responses import AttachmentJsonResponse


def render_redoc(request):
    return render(request, "docs/redoc.html")


def render_swagger_ui(request):
    return render(request, "docs/swagger_ui.html")


def json_loader(filename, subfix):
    def view(request, *args, **kwargs):
        prefix = kwargs.get("prefix")
        suffix = kwargs.get("suffix")

        prefix = [prefix] if (prefix is not None) else []
        suffix = [suffix] if (suffix is not None) else []

        location = prefix + subfix + suffix

        path = os.path.join(settings.BASE_DIR, *location)
        with open(path, "r") as file:
            file_stream = json.load(file)
        return AttachmentJsonResponse(file_stream, filename)

    return view
