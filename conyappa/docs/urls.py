from django.urls import path

from .views import json_loader, render_redoc, render_swagger_ui

app_name = "docs"

urlpatterns = [
    path("docs", render_redoc, name="render_redoc"),
    path("docs/try", render_swagger_ui, name="render_swagger_ui"),
    path("docs/openapi.json", json_loader("openapi", ["..", "docs", "openapi.json"]), name="spec"),
    path("docs/schemas/<str:suffix>", json_loader("openapi", ["..", "docs", "schemas"]), name="schema"),
]
