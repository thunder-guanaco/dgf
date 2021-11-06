from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def dgf_version():
    return settings.DGF_VERSION
