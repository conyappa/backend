import os

from django import db
from django.conf import settings

LOCATION = ["..", "sql"]
PATH = os.path.join(settings.BASE_DIR, *LOCATION)


def loads(name):
    with open(f"{PATH}/{name}.sql", mode="r") as file:
        return file.read()


def execute(code):
    with db.connection.cursor() as cursor:
        cursor.execute(code)
