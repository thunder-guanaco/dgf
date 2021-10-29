#!/bin/bash

# VIRTUALENV + DEPENDENCIES
. env/bin/activate
pip install -r requirements.txt

# SECRETS
source secrets
if [[ "$?" -eq "1" ]]
then
  echo
  echo "You should get the secrets file from the server in order to have the needed environment variables"
  echo "WARNING! This file should not be pushed to the git repository"
  exit 1
fi

# ENV
case "$1" in

  test)
    export DJANGO_ENV="test"
    ;;
  *)
    export DJANGO_ENV="dev"
    ;;
esac

# DATABASE
python manage.py migrate

# COMMAND
case "$1" in

  test)
    export DJANGO_SETTINGS_MODULE="dgf_cms.settings"
    pytest --cov=dgf --cov-config=.coveragerc --ignore=env  --flakes --pep8 -s
    ;;
  runserver)
    python manage.py runserver 0.0.0.0:8000
    ;;
  makemessages)
    python manage.py makemessages -l de -i env
    ;;
  compilemessages)
    python manage.py compilemessages -l de
    ;;
  *)
    python manage.py $1
esac
