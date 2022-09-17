import json
import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def github_issue_post_save(instance):
    url = 'https://api.github.com/repos/thunder-guanaco/dgf/issues'
    friend_name = instance.friend.short_name if instance.friend else 'Anonymous user'

    # Create our issue
    issue = {
        'title': f'{friend_name}: {instance.title}',
        'body': instance.body,
        'labels': [instance.get_type_display()]
    }

    headers = {
        'Authorization': f'token {settings.GITHUB_TOKEN}'
    }

    # Add the issue to our repository
    response = requests.post(url, json.dumps(issue), headers=headers)
    if response.status_code == 201:
        logger.info(f'Successfully created Issue "{instance.title}"')
    else:
        logger.warning(f'Could not create Issue "{instance.title}": {response.content}')
