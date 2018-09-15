#!/bin/bash

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
gunicorn pyback.wsgi -b 0.0.0.0:8000 -w 3 --access-logfile=- --error-logfile=- --capture-output