#!/bin/bash
# This script will be executed every time a deployment is started

ROOT_INSTALLATION_PATH=/home/ubuntu
cd ${ROOT_INSTALLATION_PATH}/django_project
source ci/ENVIRONMENT_VARIABLES
. ../env/bin/activate

RED="\e[31m"
GREEN="\e[32m"
RESET="\e[0m"

function exit_if_error() {
  command=$1
  return_code=$2
  if [[ "${return_code}" -ne "0" ]]
  then
    echo -e "${command}${RED}[ERROR]${RESET}"
    exit 1
  else
    echo -e "${command}${GREEN}[OK]${RESET}"
  fi
}

pip install -r requirements.txt
exit_if_error "Install dependencies" $?

yes yes | python manage.py collectstatic --clear
exit_if_error "Collect static files" $?

python manage.py compilemessages -l de
exit_if_error "Compile messages for translations" $?

python manage.py migrate
exit_if_error "Apply migrations" $?

python manage.py crontab add
exit_if_error "Add cronjobs" $?

for i in start_gunicorn.bash start_shell.bash
do
  mv ci/$i ${ROOT_INSTALLATION_PATH}
  exit_if_error "Copy script: ci/${i}" $?

  sudo chmod u+x ${ROOT_INSTALLATION_PATH}/$i
  exit_if_error "Make script executable: ci/${i}" $?
done

sudo supervisorctl restart dgf_cms
exit_if_error "Restart server" $?

