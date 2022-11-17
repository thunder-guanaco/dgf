#!/bin/bash
# This script will be executed every time a deployment is started

working_dir=$(dirname $0)
source ${working_dir}/util.bash

ROOT_INSTALLATION_PATH=/home/ubuntu
cd ${ROOT_INSTALLATION_PATH}/django_project

source ci/ENVIRONMENT_VARIABLES
. ../env/bin/activate

pip install -r requirements.txt
exit_if_error "Install dependencies" $?

python manage.py migrate
exit_if_error "Apply migrations" $?

# invalidate django compress cache
rm ${ROOT_INSTALLATION_PATH}/static/CACHE

yes yes | python manage.py collectstatic --clear
exit_if_error "Collect static files" $?

python manage.py compilemessages -l de
exit_if_error "Compile messages for translations" $?

crontab -r
exit_if_error "Delete existing cronjobs" 0

crontab ci/crontab
exit_if_error "Add new cronjobs" $?

for i in start_gunicorn.bash dgf.bash
do
  mv ci/$i ${ROOT_INSTALLATION_PATH}
  exit_if_error "Copy script: ci/${i}" $?

  sudo chmod u+x ${ROOT_INSTALLATION_PATH}/$i
  exit_if_error "Make script executable: ci/${i}" $?
done

sudo supervisorctl restart dgf_cms
exit_if_error "Restart server" $?

