#!/bin/bash

export DJANGO_ENV=test
pip install -r requirements.txt
python manage.py migrate
export DJANGO_SETTINGS_MODULE="dgf_cms.settings"
pytest --cov=dgf --cov-config=.coveragerc --ignore=env  --flakes --pep8 -s
