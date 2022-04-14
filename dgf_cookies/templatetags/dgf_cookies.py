import logging
from django import template
from django.conf import settings

from dgf_cookies.models import CookieGroupTranslation, CookieTranslation

register = template.Library()

logger = logging.getLogger(__name__)


@register.filter
def translate_cookie_group(cookie_group, language_code):
    """
    Translate the cookie_group to the given language.
    """
    if language_code == settings.DEFAULT_TRANSLATION_LANGUAGE:
        return {'name': cookie_group.name, 'description': cookie_group.description}

    translation = CookieGroupTranslation.objects.get(cookie_group=cookie_group, language=language_code)
    return {'name': translation.name, 'description': translation.description}


@register.filter
def translate_cookie(cookie, language_code):
    """
    Translate the cookie to the given language.
    """
    if language_code == settings.DEFAULT_TRANSLATION_LANGUAGE:
        return {'description': cookie.description}

    translation = CookieTranslation.objects.get(cookie=cookie, language=language_code)
    return {'description': translation.description}
