#!/bin/bash

# VIRTUALENV + DEPENDENCIES
. env/bin/activate
pip install -I -r requirements.txt

#DJANGO
python manage.py migrate

export DJANGO_ENV="dev"
export DJANGO_SECRET_KEY="it-does-not-matter-if-you-do-this-locally"
export DJANGO_DEBUG="True"
export DJANGO_ALLOWED_HOSTS="localhost"

python manage.py runserver 0.0.0.0:8000
