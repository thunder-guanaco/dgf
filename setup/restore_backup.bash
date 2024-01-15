#!/bin/bash
# This script will be executed the first time we set up the local server

working_dir=$(dirname $0)
ROOT_INSTALLATION_PATH=${working_dir}/..

cd ${ROOT_INSTALLATION_PATH}

echo "Download the following backup files from Netcup:"
echo " - dgf_db_<date>.dump"
echo " - dgf_media_<date>.tar"
read -p "Press ENTER to open Netcup's File Manager on chrome " x
google-chrome "https://a2f90.webhosting.systems/smb/file-manager/list"
read -p "Press ENTER when you finish downloading files (and leave them in the Downloads folder) " x

mkdir -p media

db_file=$(ls -t ~/Downloads/dgf_db_*.dump | head -1 | rev | cut -d '/' -f 1 | rev)
media_file=$(ls -t ~/Downloads/dgf_media_*.tar | head -1 | rev | cut -d '/' -f 1 | rev)

cp ~/Downloads/${db_file} media/
cp ~/Downloads/${media_file} media/

# CLEAR DATABASE
sudo mysql -e "DROP DATABASE dgf_cms;"
sudo mysql -e "CREATE DATABASE dgf_cms CHARACTER SET utf8;"

echo
echo "Using DB file: ${db_file}"
python manage.py dbrestore -i ${db_file}

echo
echo "Using media file: ${media_file}"
python manage.py mediarestore -i ${media_file}
