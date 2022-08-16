# Disc Golf Friends

This is a Django CMS project.

## About the technologies

* [Django](https://www.djangoproject.com/)
* [Django CMS](http://docs.django-cms.org/en/latest/index.html)

## HOWTOs

### Set up production server

See [server_setup.bash](setup/server_setup.bash)

### Set up the project to run locally

See [local_setup.bash](setup/local_setup.bash)

### Start the server

1. Activate the environment
`. env/bin/activate`

2. Install all the requirements (this could take a while the first time)
`pip install -r requirements.txt`

3. Initialize needed env vars from the secrets
`source secrets`

4. Tell application we're running locally
`export DJANGO_ENV=dev`

5. Migrate the database (this could take a while the first time)
`python manage.py migrate`

6. Run the server
`python manage.py runserver 0.0.0.0:8000`

All of this can be done at once by running the script [run.bash]
`bash run.bash runserver`

## PDGA support:

### ATTRIBUTION

Every screen of your application that contains PDGA event or player information must contain the following attribution and link to pdga.com:
Player and event data ©2015 PDGA (where 2015 is the current year)
Everywhere a player name or event name is displayed, the name must link to the player or event page at pdga.com.

## GitHub

There are 3 cases in which GitHub issues will be created:
- Feedback from a Friend
- Server error
- Management command error

The issues are created using [GitHub's API](https://docs.github.com/en).
In order to use it you'll need to add a secret called `DJANGO_GITHUB_TOKEN` containing the Personal Access Token (PAT) with the following scopes:
* `repo` → `public_repo` (Access public repositories)