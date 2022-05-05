#!/bin/bash
# This script will be executed the first time we set up the production server

ROOT_INSTALLATION_PATH=/home/ubuntu

#####################
### UPDATE SYSTEM ###
#####################

sudo apt-get update
sudo apt-get upgrade

###################
### PUBLIC KEYS ###
###################

echo "Add your public keys to .ssh/authorized_keys and DO NOT allow login via password"
read

##############
### PYTHON ###
##############

# install
sudo apt-get install python3.8 python3.8-venv python3.8-dbg python3.8-dev python3-pip ipython3 tree gettext firefox

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
pip install -r django_project/requirements.txt

#############
### MYSQL ###
#############

# Install
sudo apt-get install mysql-server libmysqlclient-dev
echo "Add a user called 'dgf' and a database called 'dgf_cms'. Check mysql_setup.sql"
read

##############
### DJANGO ###
##############

# Collect static files
yes yes | python manage.py collectstatic --clear

# Apply migrations
python manage.py migrate

################
### GUNICORN ###
################

# install
sudo apt-get install gunicorn
cp ci/start_gunicorn.bash ..
sudo chmod u+x ${ROOT_INSTALLATION_PATH}/start_gunicorn.bash

##################
### SUPERVISOR ###
##################

# install
sudo apt-get install supervisor

# configuration
cat << EOF > /etc/supervisor/conf.d/dgf_cms.conf
[program:dgf_cms]
command = ${ROOT_INSTALLATION_PATH}/start_gunicorn.bash                   ; Command to start app
user = ubuntu                                                             ; User to run as
stdout_logfile = ${ROOT_INSTALLATION_PATH}/logs/gunicorn_supervisor.log   ; Where to write log messages
redirect_stderr = true                                                    ; Save stderr in the same log
environment = LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8                         ; Set UTF-8 as default
stopasgroup = true                                                        ; cascade signals also to its children
EOF

# log folder and file for supervisor
mkdir -p ${ROOT_INSTALLATION_PATH}/logs
touch ${ROOT_INSTALLATION_PATH}/logs/gunicorn_supervisor.log

# make supervisor be aware of the new application
sudo supervisorctl reread
sudo supervisorctl update

#############
### NGINX ###
#############

# install
sudo apt-get install nginx

# start
sudo service nginx start

# configuration
echo "Use Let's Encrypt to create certificates: https://letsencrypt.org/"
echo
read
chmod 400  /etc/nginx/ssl/*
cat << EOF > /etc/nginx/conf.d/disc-golf-friends.de.conf
upstream dgf_cms_app_server {
  # fail_timeout=0 means we always retry an upstream even if it failed
  # to return a good HTTP response (in case the Unicorn master nukes a
  # single worker for timing out).

  server unix:${ROOT_INSTALLATION_PATH}/gunicorn.sock fail_timeout=0;
}

server {

    if (\$host = www.tremonia-open.de) {
        return 301 https://discgolffriends.de/turniere/tremonia-open;
    }

    if (\$host = tremonia-open.de) {
        return 301 https://discgolffriends.de/turniere/tremonia-open;
    }

    if (\$host = www.disc-golf-friends.de) {
        return 301 https://discgolffriends.de\$request_uri;
    }

    if (\$host = disc-golf-friends.de) {
        return 301 https://discgolffriends.de\$request_uri;
    }

    if (\$host = www.vps793990.ovh.net) {
        return 301 https://discgolffriends.de\$request_uri;
    }

    if (\$host = vps793990.ovh.net) {
        return 301 https://discgolffriends.de\$request_uri;
    }

    server_name disc-golf-friends.de discgolffriends.de tremonia-open.de vps793990.ovh.net www.disc-golf-friends.de www.discgolffriends.de www.tremonia-open.de www.vps793990.ovh.net;

    listen [::]:443 ssl ipv6only=on; # managed by Certbot
    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/disc-golf-friends.de/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/disc-golf-friends.de/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

    access_log ${ROOT_INSTALLATION_PATH}/logs/nginx-access.log;
    error_log ${ROOT_INSTALLATION_PATH}/logs/nginx-error.log;

    location /static/ {
        alias       ${ROOT_INSTALLATION_PATH}/static/;
        expires     1y;
        add_header  Pragma public;
        add_header  Cache-Control "public";
    }

    location /media/ {
        alias       ${ROOT_INSTALLATION_PATH}/media/;
        expires     1y;
        add_header  Pragma public;
        add_header  Cache-Control "public";
    }

    location / {
        # an HTTP header important enough to have its own Wikipedia entry:
        #   http://en.wikipedia.org/wiki/X-Forwarded-For
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;

        # enable this if and only if you use HTTPS, this helps Rack
        # set the proper protocol for doing redirects:
        # proxy_set_header X-Forwarded-Proto https;

        # pass the Host: header from the client right along so redirects
        # can be set properly within the Rack application
        proxy_set_header Host \$http_host;

        # we don't want nginx trying to do something clever with
        # redirects, we set the Host: header above already.
        proxy_redirect off;

        # set "proxy_buffering off" *only* for Rainbows! when doing
        # Comet/long-poll stuff.  It's also safe to set if you're
        # using only serving fast clients with Unicorn + nginx.
        # Otherwise you _want_ nginx to buffer responses to slow
        # clients, really.
        # proxy_buffering off;

        # Try to serve static files from nginx, no point in making an
        # *application* server like Unicorn/Rainbows! serve static files.
        if (!-f \$request_filename) {
            proxy_pass http://dgf_cms_app_server;
            break;
        }
    }

    # Error pages
    error_page 500 502 503 504 /500.html;
    location = /500.html {
        root ${ROOT_INSTALLATION_PATH}/static/;
    }

    client_max_body_size 100M;
}

server {

    if (\$host = www.tremonia-open.de) {
        return 301 https://discgolffriends.de/turniere/tremonia-open;
    }

    if (\$host = tremonia-open.de) {
        return 301 https://discgolffriends.de/turniere/tremonia-open;
    }

    if (\$host = www.disc-golf-friends.de) {
        return 301 https://discgolffriends.de\$request_uri;
    }

    if (\$host = disc-golf-friends.de) {
        return 301 https://discgolffriends.de\$request_uri;
    }

    if (\$host = www.vps793990.ovh.net) {
        return 301 https://discgolffriends.de\$request_uri;
    }

    if (\$host = vps793990.ovh.net) {
        return 301 https://discgolffriends.de\$request_uri;
    }

    listen 80 default_server;
    listen [::]:80 default_server;
    server_name disc-golf-friends.de discgolffriends.de tremonia-open.de vps793990.ovh.net www.disc-golf-friends.de www.discgolffriends.de www.tremonia-open.de www.vps793990.ovh.net;
    return 301 https://\$host\$request_uri;
}

EOF

# set dgf_cms to be the main application in nginx
ln -s /etc/nginx/sites-available/dgf_cms /etc/nginx/sites-enabled/dgf_cms
rm /etc/nginx/sites-enabled/default
service nginx restart

# data folders and nginx logs
mkdir -p ${ROOT_INSTALLATION_PATH}/{static,media,logs}
touch ${ROOT_INSTALLATION_PATH}/logs/nginx-access.log
touch ${ROOT_INSTALLATION_PATH}/logs/nginx-error.log

# give ubuntu user all the permissions in the home folder
chown -R  ubuntu ${ROOT_INSTALLATION_PATH}
