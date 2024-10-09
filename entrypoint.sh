#! /bin/bash

# Exit emmediately on error
set -e

python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py light_setup

python manage.py runserver 0.0.0.0:8000
