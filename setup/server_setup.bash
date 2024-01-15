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

echo "Add your public key(s)"
echo -n "Press ENTER to edit .ssh/authorized_keys "
read
vim .ssh/authorized_keys
echo
echo "Now disable ssh login via password authentication by editing"
echo -n "Press ENTER to edit /etc/ssh/sshd_config "
read
sudo vim /etc/ssh/sshd_config

###############
### SECRETS ###
###############

echo "Fill all the needed secrets (see secrets_template or your local secrets file [NEVER COMMIT THIS])"
echo -n "Press ENTER to edit secrets "
read
vim secrets

#############
### MYSQL ###
#############

# Install
yes | sudo apt-get install mysql-server-8.0 libmysqlclient-dev
echo "Add a user called 'dgf' and a database called 'dgf_cms'. Check mysql_setup.sql"
echo -n "Press ENTER to enter the mysql console "
read
sudo mysql -u root

##############
### PYTHON ###
##############

# install
yes |sudo apt-get install python3.10 python3.10-venv python3.10-dbg python3.10-dev python3-pip ipython3 tree gettext firefox

# create virtualenv
cd ${ROOT_INSTALLATION_PATH}
python3.10 -m venv env

# activate the virtual environment
. ./env/bin/activate

# upgrade pip
pip install --upgrade pip

# basic dependencies
pip install wheel==0.41.3
pip install svglib==1.1.0 # newer versions are not ok

##############
### DJANGO ###
##############

echo "Now you should copy the project to the server, preferably in the folder ${ROOT_INSTALLATION_PATH} using deploy.yml stuff"
echo -n "Press ENTER when you are done "
read

bash ${ROOT_INSTALLATION_PATH}/django_project/ci/server_restart.bash

echo "Now you download the backup files (dgf_db...dump and dg_media...tar), copy them to the server, preferably in the folder ${ROOT_INSTALLATION_PATH} and restore them"
echo -n "Press ENTER when you are done "
read

# clear database
sudo mysql -e "DROP DATABASE dgf_cms;"
sudo mysql -e "CREATE DATABASE dgf_cms CHARACTER SET utf8;"

# restore database and media
bash dgf.bash dbrestore -I ${ROOT_INSTALLATION_PATH}/dgf_db_*.dump
bash dgf.bash mediarestore -I ${ROOT_INSTALLATION_PATH}/dgf_media_*.tar


################
### GUNICORN ###
################

# install
yes |sudo apt-get install gunicorn

# either execute the following 3 lines yourself or let the deploy script do it
cd ${ROOT_INSTALLATION_PATH}/django_project
cp ci/start_gunicorn.bash ..
sudo chmod u+x ${ROOT_INSTALLATION_PATH}/start_gunicorn.bash

##################
### SUPERVISOR ###
##################

# install
yes | sudo apt-get install supervisor

# configuration
sudo touch /etc/supervisor/conf.d/dgf_cms.conf
sudo chown ubuntu  /etc/supervisor/conf.d/dgf_cms.conf
cat << EOF > /etc/supervisor/conf.d/dgf_cms.conf
[program:dgf_cms]
command = ${ROOT_INSTALLATION_PATH}/start_gunicorn.bash                   ; Command to start app
user = ubuntu                                                             ; User to run as
stdout_logfile = ${ROOT_INSTALLATION_PATH}/logs/gunicorn_supervisor.log   ; Where to write log messages
redirect_stderr = true                                                    ; Save stderr in the same log
environment = LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8                         ; Set UTF-8 as default
stopasgroup = true                                                        ; cascade signals also to its children
EOF
sudo chown root  /etc/supervisor/conf.d/dgf_cms.conf

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
yes | sudo apt-get install nginx

# start
sudo service nginx restart
#sudo chmod 400  /etc/nginx/ssl/*
sudo touch /etc/nginx/conf.d/disc-golf-friends.de.conf
sudo chown ubuntu /etc/nginx/conf.d/disc-golf-friends.de.conf
cat << EOF > /etc/nginx/conf.d/disc-golf-friends.de.conf
upstream dgf_cms_app_server {
    # fail_timeout=0 means we always retry an upstream even if it failed
    # to return a good HTTP response (in case the Unicorn master nukes a
    # single worker for timing out).

    server unix:${ROOT_INSTALLATION_PATH}/gunicorn.sock fail_timeout=0;
}

server {

    if (\$host = www.tremonia-open.de) {
        return 301 https://discgolffriends.de/turniere/tremonia-open\$request_uri;
    }

    if (\$host = tremonia-open.de) {
        return 301 https://discgolffriends.de/turniere/tremonia-open\$request_uri;
    }

    server_name discgolffriends.de tremonia-open.de www.discgolffriends.de www.tremonia-open.de;

    access_log ${ROOT_INSTALLATION_PATH}/logs/nginx-access.log;
    error_log ${ROOT_INSTALLATION_PATH}/logs/nginx-error.log;

    location /static/ {
        alias       ${ROOT_INSTALLATION_PATH}/static/;
        expires     1y;
        add_header  Pragma public;
        add_header  Cache-Control "public";
        add_header  Access-Control-Allow-Origin https://discgolfmetrix.com;
    }

    location /media/ {
        alias       ${ROOT_INSTALLATION_PATH}/media/;
        expires     1y;
        add_header  Pragma public;
        add_header  Cache-Control "public";
        add_header  Access-Control-Allow-Origin https://discgolfmetrix.com;
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
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name disc-golf-friends.de discgolffriends.de tremonia-open.de www.discgolffriends.de www.tremonia-open.de;
    return 301 https://\$host\$request_uri;
}
EOF

sudo chown root /etc/nginx/conf.d/disc-golf-friends.de.conf

# set dgf_cms to be the main application in nginx
sudo rm /etc/nginx/sites-enabled/default
sudo rm /etc/nginx/sites-available/default

# kill nginx, kill it well
sudo pkill -f nginx
sudo systemctl start nginx
sudo service nginx start

# data folders and nginx logs
mkdir -p ${ROOT_INSTALLATION_PATH}/{static,media,logs}
touch ${ROOT_INSTALLATION_PATH}/logs/nginx-access.log
touch ${ROOT_INSTALLATION_PATH}/logs/nginx-error.log

# give ubuntu user all the permissions in the home folder
chown -R ubuntu ${ROOT_INSTALLATION_PATH}
chmod 755 ${ROOT_INSTALLATION_PATH}

###################
### CERTIFICATE ###
###################

echo "Set up discgolffriends.de and tremonia-open.de to point to this server before continuing"

# stop nginx
sudo service nginx stop

# install
yes | sudo apt-get install certbot python3-certbot-nginx

# configuration
echo "Use Let's Encrypt to create certificates: https://letsencrypt.org/"
echo -n "Press ENTER to create a certificate "
read
sudo certbot --nginx -d discgolffriends.de -d tremonia-open.de

#reload nginx
sudo service nginx reload

echo "Save the content of the nginx configuration somewhere, please"
echo -n "Press ENTER to show the contents of /etc/nginx/conf.d/disc-golf-friends.de.conf "
read
sudo cat /etc/nginx/conf.d/disc-golf-friends.de.conf