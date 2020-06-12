#!/bin/bash
# This script helps you start the django shell

ROOT_INSTALLATION_PATH=/home/ubuntu
cd ${ROOT_INSTALLATION_PATH}/django_project

source ci/ENVIRONMENT_VARIABLES

# Activate the virtual environment
. ../env/bin/activate

python manage.py shell