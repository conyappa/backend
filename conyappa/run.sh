#!/bin/bash

python manage.py migrate

if [ "$DJANGO_ENV" = "development" ]; then
  exec gunicorn --bind 0.0.0.0:$PORT main.wsgi --reload --log-level debug
else
  exec gunicorn --bind 0.0.0.0:$PORT main.wsgi --log-level info
fi
