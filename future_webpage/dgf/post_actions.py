import json

import requests
from django.conf import settings


def feedback_post_save(instance):
    url = 'https://api.github.com/repos/thunder-guanaco/dgf/issues'

    # Create our issue
    issue = {
        'title': '{}: {}'.format(instance.friend.short_name, instance.title),
        'body': instance.feedback,
        'labels': ['Feedback']
    }
    headers = {
        'Authorization': 'token {}'.format(settings.GITHUB_TOKEN)
    }

    # Add the issue to our repository
    response = requests.post(url, json.dumps(issue), headers=headers)
    if response.status_code == 201:
        print('Successfully created Issue "{}"'.format(instance.title))
    else:
        print('Could not create Issue "{}"'.format(instance.title))
