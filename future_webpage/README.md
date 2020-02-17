# Disc Golf Friends

This is a Django CMS project.

## About the technologies

* [Django](https://www.djangoproject.com/)
* [Django CMS](http://docs.django-cms.org/en/latest/index.html)

## HOWTOs

### Set up the project

1. Install virtualenv
`sudo apt-get install virtualenv`

1. Create an environment
`virtualenv env`


### Start the server

1. Activate the environment
`. env/bin/activate`

1. Install all the requirements (this could take a while the first time)
`pip install -r requirements.txt`

1. Migrate the database (this could take a while the first time)
`python manage.py migrate`

1. Run the server
`python manage.py runserver`

All of this can be done at once by running the script [run.bash]


## PDGA support:

### ATTRIBUTION

Every screen of your application that contains PDGA event or player information must contain the following attribution and link to pdga.com:
Player and event data ©2015 PDGA (where 2015 is the current year)
Everywhere a player name or event name is displayed, the name must link to the player or event page at pdga.com.

