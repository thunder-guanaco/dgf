#!/bin/bash

# VIRTUALENV + DEPENDENCIES
. env/bin/activate
pip install -r requirements.txt

#DJANGO
export DJANGO_ENV="test"
python manage.py test
