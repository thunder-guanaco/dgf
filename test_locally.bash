#!/bin/bash

export DJANGO_ENV="test"
export DJANGO_SETTINGS_MODULE="dgf_cms.settings"

source secrets
source env/bin/activate

pip install -r requirements.txt
python manage.py migrate

pytest --cov=dgf --cov-config=.coveragerc --ignore=env  --flakes --pep8 -s
