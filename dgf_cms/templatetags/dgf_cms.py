from json import dumps

from django import template
from django.conf import settings
from django.core.serializers import serialize
from django.db.models import Q
from django.db.models.query import QuerySet
from filer.models.imagemodels import Image

register = template.Library()


@register.simple_tag
def dgf_version():
    return settings.DGF_VERSION


@register.filter
def is_reviewer(user):
    if user is None:
        return False
    return user.groups.filter(name=settings.REVIEWER_GROUP).exists()


@register.simple_tag
def random_background_img_url(friend):
    all_images = Image.objects.filter(folder__name=settings.BACKGROUND_FOLDER)

    if friend:
        all_images = all_images.filter(original_filename__startswith=f'{friend.username}.')

    background_image = all_images.order_by('?').first()
    return background_image.url if background_image else ''


@register.filter
def json(object):
    if isinstance(object, QuerySet):
        return serialize('json', object)
    return dumps(object)


@register.filter
def minimum(a, b):
    return min(a, b)


@register.filter
def divided_by(a, b):
    return a / b


@register.filter
def order_by(queryset, ordering):
    order_list = ordering.split(',')
    for order in order_list:
        attribute = order[1:] if order[0] == '-' else order
        query = Q(**{f'{attribute}__isnull': False})
        queryset = queryset.filter(query)
    return queryset.order_by(*order_list)
