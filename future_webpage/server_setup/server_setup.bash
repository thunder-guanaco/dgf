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
sudo apt-get install python3
sudo apt-get install python3-venv 
sudo apt-get install python3-pip 
pip3 install -U pip

# create virtualenv
cd ${ROOT_INSTALLATION_PATH}
python3 -m venv env

# Activate the virtual environment
. ../env/bin/activate

# Install dependencies
pip install -r requirements.txt

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
environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8                           ; Set UTF-8 as default encoding
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
cat << EOF > /etc/nginx/sites-available/dgf_cms
upstream dgf_cms_app_server {
  # fail_timeout=0 means we always retry an upstream even if it failed
  # to return a good HTTP response (in case the Unicorn master nukes a
  # single worker for timing out).

  server unix:${ROOT_INSTALLATION_PATH}/gunicorn.sock fail_timeout=0;
}

server {

    listen   80;
    server_name vps793990.ovh.net;

    client_max_body_size 4G;

    access_log ${ROOT_INSTALLATION_PATH}/logs/nginx-access.log;
    error_log ${ROOT_INSTALLATION_PATH}/logs/nginx-error.log;

    location /static/ {
        alias   ${ROOT_INSTALLATION_PATH}/static/;
    }

    location /media/ {
        alias   ${ROOT_INSTALLATION_PATH}/media/;
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
