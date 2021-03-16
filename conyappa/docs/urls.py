from django.urls import path

from .views import render_docs, json_loader

app_name = "docs"

urlpatterns = [
    path("", render_docs, name="render"),
    path("openapi.json", json_loader("openapi", ["..", "docs", "openapi.json"]), name="spec"),
    path("schemas/<str:suffix>", json_loader("openapi", ["..", "docs", "schemas"]), name="schema"),
]
