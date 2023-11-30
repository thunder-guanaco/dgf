#!/bin/bash

# VIRTUALENV + DEPENDENCIES
. env/bin/activate

last_arg="${@: -1}"
if [[ "${last_arg}" != "fast" ]]
then
  pip install -r requirements.txt
else
  echo ">>> fast mode, no requirements install"
fi

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
if [[ "${last_arg}" != "fast" ]]
then
  python manage.py migrate
else
  echo ">>> fast mode, no migrations"
fi

# COMMAND
case "$1" in

  test)
    export DJANGO_SETTINGS_MODULE="dgf_cms.settings"
    pytest --cov=dgf --cov=dgf_league --cov-config=.coveragerc --cov-report term-missing --ignore=env  --flakes --flake8 -s
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
    if [[ "${last_arg}" != "fast" ]]
    then
      args=$@
    else
      args="${@:1:$(($#-1))}"
    fi
    python manage.py $args
esac
