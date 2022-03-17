# Disc Golf Friends

This is a Django CMS project.

## About the technologies

* [Django](https://www.djangoproject.com/)
* [Django CMS](http://docs.django-cms.org/en/latest/index.html)

## HOWTOs

### Set up production server

See `server_setup.bash`

### Set up the project to run locally

1. Install virtualenv

`sudo apt-get install python3-virtualenv`

1. Create an environment
`python3 -m venv ./env`

1. Install MySQL and create the necessary user and tables (this code works with MySQL 8)
```bash
sudo apt-get install mysql-server libmysqlclient-dev
sudo mysql -e "CREATE USER 'dgf'@'localhost' IDENTIFIED BY 'dgf';
sudo mysql -e "CREATE DATABASE dgf_cms;"
sudo mysql -e "GRANT ALL PRIVILEGES ON dgf_cms.* TO 'dgf'@'localhost' WITH GRANT OPTION;"
```

### Start the server

1. Activate the environment
`. env/bin/activate`

1. Install all the requirements (this could take a while the first time)
`pip install -r requirements.txt`

1. Migrate the database (this could take a while the first time)
`python manage.py migrate`

1. Tell application we're running locally
`export DJANGO_ENV=dev`

1. Run the server
`python manage.py runserver 0.0.0.0:8000`

All of this can be done at once by running the script [run.bash]


## PDGA support:

### ATTRIBUTION

Every screen of your application that contains PDGA event or player information must contain the following attribution and link to pdga.com:
Player and event data ©2015 PDGA (where 2015 is the current year)
Everywhere a player name or event name is displayed, the name must link to the player or event page at pdga.com.

