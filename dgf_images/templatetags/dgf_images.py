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
