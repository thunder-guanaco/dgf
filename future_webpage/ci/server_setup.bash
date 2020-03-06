#!/bin/bash

ROOT_INSTALLATION_PATH=/home/ubuntu

#####################
### UPDATE SYSTEM ###
#####################

sudo apt-get update
sudo apt-get upgrade

###################
### PUBLIC KEYS ###
###################

cat << EOF >> .ssh/authorized_keys
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDZZuJMNyM8AbrBMnTjMa4TfgFXC+8+en/otrErjG8mPCcEnPCe4MyIh2GJqEZSC5OFZXBmZqqYvLpMogRrffY4tnfXQ8QBOhFhWKUh8H6JNTXpj32L5Bbt9y9VPPENXh+opL1wdE1Ik1lsQl7ngmI/kiXI1SKNzxmBykxA14a23LlorzPMjJF9CXzaA4oYflk27ydsd63CLwxByQjiRGCAPNSLu6k1ozjCGgMa5Uz+7s5+opBdKmnZy/L5+G416PWdMe55o3SkuzzPDKC8jI6IdIoMTEG7EnxSel7gkQxAOc/ViVPGuW0f2rtoQs48WOcXHSCqNI1on0O7X2vLMHYgEnyv4kUc51hG7elLnM3CePTF6iLiQQS9iHj9GYZVs8J62UrpSPoSR6nuCPyLfXdi+N4DWsWAAz7gWkI6SqS4ezQeM1Hb2rMXyec7lnyFFHn7g2hrbNt94DhRglqqJow0PHt7fIcJWNefsoo6oXmxXRvwuuZreqiLsYnfGWcRGnM= manolo@pfau
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3AZpewhkY8rC/RMnHLw1JoUY5vj6P2WVkL6Jq6RDMycE3LyS8TZLDh8NiTbVxV3aObHQIFPr1qndXmrQ5Yz2BHmnGMNnbcYqG5JU++Tjvakq5lf83n1WamJJzHL1k8SFTi30UnKnbtesXyfWpyGx6Hp0MONJ4+zev9sFClkckC1yAApUqFQxpD8Z4STFbZuf+sRtJlTlxonZQqLN4mSLPsPn6bmmw2Krut+zUXo7bgsvyyB1hBNwlil/3ab02MLIR6/+JMQVctqE7cI0/I8WLxtPbFZ7KZGuS/rDmEz6WCzClvzPf3TfZk95vpNqzdaId46Z6LDURk4b/adsqoCnL fes@foryouandyourcustomers.com
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDGYI6qrehlcmgZ89pu5fEEd+7cEAHU8qtewhwp5pmfkQN7pkvmwsDpqKhbX+bi9WQjXwxv6KEkDWavBnYj16BiJkrcdlVmcw2zFh+wIKZrIXhsPIecyg4rKCFRgtvqjUNNwquQ7EpWo4FnQwTRWMcFDyZDlvRnDwGeW25UUCo+C3jjNdkHWNRgT0NoZd5a/Kcp2y/ILkL7e4MIwrgZ+fwMFxedGGNchYSa+mwkiu6HVfEj3FsTkj23H6W8kgN7yqeTLP627f4gxHcoueWPQDFfoW2LtewCVWRt1AhyxeCTP4/ycBOzSj02J0p8HaDUBMp5LDLo7kgxawBUsIk8btCq1VoISAgJneoOdrfWqM5XPRdv1izjJKZY2syyzD+Yw5je8Ue+jykKWwRHDUAO/SP3dhYyv3PHa3VeKlPavU4SqbK8NYhVxCT35XTK9ttP35jvvREH8oinZttl8+RpukBfL5bXhmekbGgs9adsknAXgXiGJu21Bx+f2zyA6gB/mz0= github
EOF

##############
### PYTHON ###
##############

# install
sudo apt-get install python3
sudo apt-get install python3-venv 
sudo apt-get install python3-pip 
pip3 install -U pip

# create virtualenv
cd ${ROOT_PATH}
python3 -m venv env

################
### GUNICORN ###
################

# install
sudo apt-get install gunicorn

# create run script and allow it to be executed
cat << EOF > ${ROOT_INSTALLATION_PATH}/start_gunicorn.bash
#!/bin/bash

echo "Starting Disc Golf Friends CMS application (dgf_cms)"

# ENVIRONMENT VARIABLES
export DJANGO_ENV="prod"
export DJANGO_SECRET_KEY="delete-me-and-take-this-from-a-file"
export DJANGO_DEBUG="False"
export DJANGO_ALLOWED_HOSTS="vps793990.ovh.net"

cd ${ROOT_INSTALLATION_PATH}/django_project

# Activate the virtual environment
. ../env/bin/activate

# Apply migrations (if necessary)
python manage.py migrate

# Start Django Unicorn
gunicorn dgf_cms.wsgi:application \
  --name "dgf_cms" \
  --workers 3 \
  --user=ubuntu \
  --bind=unix:${ROOT_INSTALLATION_PATH}/gunicorn.sock \
  --log-level=debug \
  --log-file=- 
EOF

sudo chmod u+x ${ROOT_INSTALLATION_PATH}/start_gunicorn.bash

##################
### SUPERVISOR ###
##################

# install
sudo apt-get install supervisor

# configuration
cat << EOF > /etc/supervisor/conf.d/dgf_cms.conf
[program:dgf_cms]
command = ${ROOT_INSTALLATION_PATH}/start_gunicorn.bash                  ; Command to start app
user = ubuntu                                               ; User to run as
stdout_logfile = ${ROOT_INSTALLATION_PATH}/logs/gunicorn_supervisor.log  ; Where to write log messages
redirect_stderr = true                                      ; Save stderr in the same log
environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8             ; Set UTF-8 as default encoding
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

# data folders
mkdir -p ${ROOT_INSTALLATION_PATH}/{static,media,logs}
touch ${ROOT_INSTALLATION_PATH}/logs/nginx-access.log
touch ${ROOT_INSTALLATION_PATH}/logs/nginx-error.log

