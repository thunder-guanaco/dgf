#!/bin/bash

# VIRTUALENV + DEPENDENCIES
. env/bin/activate
pip install -r requirements.txt

#DJANGO
export DJANGO_ENV="dev"
python manage.py makemessages -l de -i env
