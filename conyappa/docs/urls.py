from django.urls import path

from .views import json_loader, render_docs

app_name = "docs"

urlpatterns = [
    path("docs", render_docs, name="render"),
    path("docs/openapi.json", json_loader("openapi", ["..", "docs", "openapi.json"]), name="spec"),
    path("docs/schemas/<str:suffix>", json_loader("openapi", ["..", "docs", "schemas"]), name="schema"),
]
