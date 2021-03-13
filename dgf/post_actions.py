import json

import requests


def feedback_post_save(instance):
    url = 'https://api.github.com/repos/thunder-guanaco/dgf/issues'
    friend_name = instance.friend.short_name if instance.friend else 'Anonymous user'

    # Create our issue
    issue = {
        'title': f'{friend_name}: {instance.title}',
        'body': instance.feedback,
        'labels': ['Feedback']
    }
    headers = {
        f'Authorization': 'token {settings.GITHUB_TOKEN}'
    }

    # Add the issue to our repository
    response = requests.post(url, json.dumps(issue), headers=headers)
    if response.status_code == 201:
        print(f'Successfully created Issue "{instance.title}"')
    else:
        print(f'Could not create Issue "{instance.title}"')
