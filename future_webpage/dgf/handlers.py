from django.views import defaults

from .models import Feedback


def nice_format(dictionary):
    return '\n'.join(['* **{}**: {}'.format(key, value) for key, value in dictionary.items()])


def server_error(request):
    headers = nice_format(request.headers)
    body = nice_format(request.POST) if request.method == 'POST' else ' -- '
    friend = request.user.friend if not request.user.is_anonymous else None
    Feedback.objects.create(title='Server error on {} {}'.format(request.method, request.get_full_path()),
                            feedback='# Headers\n{}\n'
                                     '# Body\n{}'.format(headers, body),
                            friend=friend)

    return defaults.server_error(request)
