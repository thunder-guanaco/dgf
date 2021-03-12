from django.views import defaults

from .models import Feedback


def nice_format(dictionary):
    return '\n'.join([f'* **{key}**: {value}' for key, value in dictionary.items()])


def server_error(request):
    headers = nice_format(request.headers)
    body = nice_format(request.POST) if request.method == 'POST' else ' -- '
    friend = request.user.friend if not request.user.is_anonymous else None
    Feedback.objects.create(title=f'Server error on {request.method} {request.get_full_path()}',
                            feedback=f'# Headers\n{headers}\n# Body\n{body}',
                            friend=friend)

    return defaults.server_error(request)
