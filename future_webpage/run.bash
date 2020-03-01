#!/bin/bash

# VIRTUALENV + DEPENDENCIES
. env/bin/activate
pip3 install -r requirements.txt

#DJANGO
python3 manage.py migrate
export DJANGO_ENV="prod"
export DJANGO_SECRET_KEY="delete-me"
export DJANGO_DEBUG="True"
export DJANGO_ALLOWED_HOSTS="vps793990.ovh.net"
python3 manage.py runserver 0.0.0.0:8080
