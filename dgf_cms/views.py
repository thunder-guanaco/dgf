import logging

from django.shortcuts import redirect

logger = logging.getLogger(__name__)


def csrf_failure(request, reason=""):
    logger.warning(f'CSRF failure after login from {request.user}: {reason}')
    url = request.GET.get('next') or '/'
    return redirect(url)
