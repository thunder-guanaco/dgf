#!/bin/bash

python manage.py collectstatic
supervisorctl restart dgf_cms
service nginx restart
