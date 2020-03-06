#!/bin/bash

# VIRTUALENV + DEPENDENCIES
. env/bin/activate
pip install -r requirements.txt

#DJANGO
python manage.py migrate
export DJANGO_ENV="dev"
python manage.py runserver 0.0.0.0:8000
