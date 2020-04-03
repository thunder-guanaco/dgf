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

# Compile messages for translations
python manage.py compilemessages -l de

# Apply migrations
python manage.py migrate

# Add cronjobs
python manage.py crontab add

# Copy scripts
for i in start_gunicorn.bash start_shell.bash
do
  mv ci/$i ${ROOT_INSTALLATION_PATH}
  sudo chmod u+x ${ROOT_INSTALLATION_PATH}/$i
done

# Restart server
sudo supervisorctl restart dgf_cms

