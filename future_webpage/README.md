# Disc Golf Friends

This is a Django CMS project.

## About the technologies

* [Django](https://www.djangoproject.com/)
* [Django CMS](http://docs.django-cms.org/en/latest/index.html)

## HOWTOs

### Set up server

See `server_setup.bash`

### Set up the project to run locally

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

1. Tell application we're running locally
`export DJANGO_ENV=dev`

1. Run the server
`python manage.py runserver 0.0.0.0:8000`

All of this can be done at once by running the script [run_locally.bash]

