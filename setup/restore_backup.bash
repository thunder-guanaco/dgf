#!/bin/bash
# This script will be executed the first time we set up the local server

working_dir=$(dirname $0)
ROOT_INSTALLATION_PATH=${working_dir}/..

cd ${ROOT_INSTALLATION_PATH}

echo "Download the following backup files from Netcup:"
echo " - dgf_db_<date>.dump"
echo " - dgf_media_<date>.tar"
read -p "Press ENTER to open Ionos' File Manager on chrome "
google-chrome "https://mein.ionos.de/webhosting/2e73d4d8-0017-4794-b4ac-ce73b8823f86/webspace-explorer"
read -p "Press ENTER when you finish downloading files (and leave them in the Downloads folder) "

mkdir -p media

db_file=$(ls -t ~/Downloads/dgf_db_*.dump | head -1 | rev | cut -d '/' -f 1 | rev)
media_file=$(ls -t ~/Downloads/dgf_media_*.tar | head -1 | rev | cut -d '/' -f 1 | rev)

cp ~/Downloads/${db_file} media/
cp ~/Downloads/${media_file} media/

# CLEAR DATABASE
sudo mysql -e "DROP DATABASE dgf_cms; CREATE DATABASE dgf_cms CHARACTER SET utf8;"

python manage.py dbrestore -i ${db_file}
python manage.py mediarestore -i ${media_file}
