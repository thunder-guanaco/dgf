#!/bin/bash
# This script will be executed the first time we set up the local server

working_dir=$(dirname $0)
ROOT_INSTALLATION_PATH=${working_dir}/..

#####################
### UPDATE SYSTEM ###
#####################

sudo apt-get update

##############
### PYTHON ###
##############

# install
sudo apt-get install python3 python3-venv python3-dbg python3-dev python3-pip ipython3 tree gettext firefox

# create virtualenv
cd ${ROOT_INSTALLATION_PATH}
python3 -m venv env

# activate the virtual environment
. ./env/bin/activate

# upgrade pip
pip install --upgrade pip

# basic dependencies
pip install wheel
pip install svglib==1.1.0 # newer versions are not ok

# install dependencies
pip install -r requirements.txt

###############
### SECRETS ###
###############

scp ubuntu@vps793990.ovh.net:secrets .
source secrets

#############
### MYSQL ###
#############

sudo apt-get install mysql-server libmysqlclient-dev
sudo mysql -e "CREATE USER 'dgf'@'localhost' IDENTIFIED BY 'dgf';"
sudo mysql -e "CREATE DATABASE dgf_cms CHARACTER SET utf8;"
sudo mysql -e "GRANT ALL PRIVILEGES ON dgf_cms.* TO 'dgf'@'localhost' WITH GRANT OPTION;"

##############
### DJANGO ###
##############

# Tell application we're running locally
export DJANGO_ENV=dev

read -p "Do you want to restore a previous backup? [Y/n] " answer
answer=${answer:-Y}
if [[ ${answer} =~ ^[Yy]$ ]]
then
  bash ${ROOT_INSTALLATION_PATH}/setup/restore_backup.bash
else
  python manage.py migrate.
fi

