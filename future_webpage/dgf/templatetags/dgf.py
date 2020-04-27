from datetime import datetime

from django import template
from django.db.models import Count

from ..models import Ace, Friend, DiscInBag

register = template.Library()

AMOUNT_OF_FAVORITE_DISCS = 3


@register.simple_tag
def favorite_course():
    return Friend.objects.filter(favorite_course__isnull=False) \
        .values('favorite_course__name') \
        .annotate(count=Count('favorite_course__name')) \
        .order_by('-count').first()['favorite_course__name']


@register.simple_tag
def all_aces():
    return Ace.objects.all()


@register.filter
def before_current_year(aces):
    return aces.filter(date__year__lt=datetime.now().year).count()


@register.filter
def before_current_year_tournaments(aces):
    return aces.filter(date__year__lt=datetime.now().year, type=Ace.TOURNAMENT).count()


@register.filter
def current_year(aces):
    return aces.filter(date__year=datetime.now().year).count()


@register.filter
def current_year_tournaments(aces):
    return aces.filter(date__year=datetime.now().year, type=Ace.TOURNAMENT).count()


@register.simple_tag
def favorite_discs(disc_type):
    return DiscInBag.objects.filter(type=disc_type) \
        .values('disc__display_name') \
        .annotate(count=Count('disc__display_name')) \
        .order_by('-count')[:AMOUNT_OF_FAVORITE_DISCS] \
        .values_list('disc__display_name', flat=True)
