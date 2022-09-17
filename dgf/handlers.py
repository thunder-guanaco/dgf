import json

from django.views import defaults

from .models import GitHubIssue

SENSITIVE_INFO = ['Cookie', 'csrfmiddlewaretoken', 'sessid']


def _filter_sensible_info_out(value):
    return {key: value for key, value in value.items() if key not in SENSITIVE_INFO}


def nice_json_format(value):
    return f'```\n{json.dumps(_filter_sensible_info_out(value), indent=2)}\n```'


def nice_format(dictionary):
    return '\n'.join([f'* **{key}**: {value}' for key, value in _filter_sensible_info_out(dictionary).items()])


def server_error(request):
    headers = nice_format(request.headers)
    body = nice_format(request.POST) if request.method == 'POST' else ' -- '
    friend = request.user.friend if not request.user.is_anonymous else None
    GitHubIssue.objects.create(title=f'Server error on {request.method} {request.get_full_path()}',
                               body=f'# Headers\n{headers}\n# Body\n{body}',
                               friend=friend,
                               type=GitHubIssue.LIVE_ERROR)

    return defaults.server_error(request)
