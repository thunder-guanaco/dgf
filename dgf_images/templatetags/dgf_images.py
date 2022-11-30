import logging

from django import template

from dgf.models import Friend

register = template.Library()

logger = logging.getLogger(__name__)


@register.simple_tag
def all_friends():
    return Friend.objects \
        .filter(social_media_agreement=True) \
        .exclude(main_photo__isnull=True) \
        .exclude(main_photo='') \
        .order_by('?')


@register.simple_tag
def all_pdga_friends():
    return Friend.objects \
        .filter(social_media_agreement=True) \
        .exclude(pdga_number__isnull=True) \
        .exclude(main_photo__isnull=True) \
        .exclude(main_photo='') \
        .order_by('?')


@register.filter
def replace(value, arg):
    """
    Replace characters inside string
    Usage `{{ "aaa"|replace:"a|b" }}`
    """
    replacement = arg.split('|')
    if len(replacement) != 2:
        return value

    what, to = replacement
    return value.replace(what, to)


@register.filter
def mobile_or_desktop(request, arg):
    """
    Returns first value if mobile and the second if desktop
    Usage `{{ request|mobile_or_desktop:"25|50" }}`
    """
    values = arg.split('|')
    if len(values) != 2:
        raise ValueError('Unexpected value. Expected something like "25|50"')

    mobile, desktop = values
    return mobile if request.user_agent.is_mobile else desktop
