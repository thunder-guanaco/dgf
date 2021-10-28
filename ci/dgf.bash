#!/bin/bash
# This script helps you go to the environment of the DGF django project and run a command if you want

ROOT_INSTALLATION_PATH=/home/ubuntu
cd ${ROOT_INSTALLATION_PATH}/django_project

source ci/ENVIRONMENT_VARIABLES
. ../env/bin/activate

if [ "$#" -ne 0 ]
then
    python manage.py "$@"
else
    python manage.py help
    echo
    echo "You didn't type any command. See the list above"
    echo
    exit 1
fi