#!/bin/bash
# This script will be executed when we start gunicorn

ROOT_INSTALLATION_PATH=/home/ubuntu
cd ${ROOT_INSTALLATION_PATH}/django_project

source ci/ENVIRONMENT_VARIABLES

# Activate the virtual environment
. ../env/bin/activate

# Start Django Unicorn
echo "Starting Disc Golf Friends CMS application (dgf_cms)"
gunicorn dgf_cms.wsgi:application \
  --name "dgf_cms" \
  --workers 3 \
  --user=ubuntu \
  --bind=unix:${ROOT_INSTALLATION_PATH}/gunicorn.sock \
  --log-level=debug \
  --log-file=-

