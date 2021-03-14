#!/bin/bash
# This script will be executed every time BEFORE a deployment is started

working_dir=$(dirname $0)
source ${working_dir}/util.bash

ROOT_INSTALLATION_PATH=/home/ubuntu
cd ${ROOT_INSTALLATION_PATH}/django_project

source ci/ENVIRONMENT_VARIABLES
. ../env/bin/activate

python manage.py backup
exit_if_error "DB and media backup" $?
