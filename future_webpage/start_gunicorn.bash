#!/bin/bash

ROOT_INSTALLATION_PATH=/home/ubuntu

echo "Starting Disc Golf Friends CMS application (dgf_cms)"

# ENVIRONMENT VARIABLES
export DJANGO_ENV="prod"
export DJANGO_SECRET_KEY="delete-me-and-take-this-from-a-file"
export DJANGO_DEBUG="False"
export DJANGO_ALLOWED_HOSTS="vps793990.ovh.net"

cd ${ROOT_INSTALLATION_PATH}/django_project

# Activate the virtual environment
. ../env/bin/activate

python manage.py collectstatic

# Apply migrations (if necessary)
python manage.py migrate

# Start Django Unicorn
gunicorn dgf_cms.wsgi:application \
  --name "dgf_cms" \
  --workers 3 \
  --user=ubuntu \
  --bind=unix:${ROOT_INSTALLATION_PATH}/gunicorn.sock \
  --log-level=debug \
  --log-file=-
EOF

