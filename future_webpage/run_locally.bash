#!/bin/bash

# VIRTUALENV + DEPENDENCIES
. env/bin/activate
pip install -r requirements.txt

#DJANGO
python manage.py migrate
export DJANGO_ENV="dev"
source pdga.cnf
if [[ "$?" -eq "1" ]]
then
  echo
  echo "You should get the pdga.cnf file from the server in order to have the needed environment variables"
  echo "WARNING! This file should not be pushed to the git repository"
  exit 1
fi
python manage.py runserver 0.0.0.0:8000
