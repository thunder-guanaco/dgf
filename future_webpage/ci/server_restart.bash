#!/bin/bash
# This script will be executed every time a deployment is started

ROOT_INSTALLATION_PATH=/home/ubuntu
cd ${ROOT_INSTALLATION_PATH}/django_project

source ci/ENVIRONMENT_VARIABLES

# Activate the virtual environment
. ../env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Collect static files
yes yes | python manage.py collectstatic --clear

# Apply migrations
python manage.py migrate

# Copy start script
mv ci/start_gunicorn.bash ..
sudo chmod u+x ${ROOT_INSTALLATION_PATH}/start_gunicorn.bash

# Restart server
sudo supervisorctl restart dgf_cms

