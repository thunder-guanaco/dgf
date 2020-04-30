from datetime import datetime

from django import template
from django.db.models import Count

from ..models import Ace, Friend, DiscInBag

register = template.Library()

AMOUNT_OF_FAVORITE_DISCS = 3
AMOUNT_OF_FAVORITE_COURSES = 3
AMOUNT_OF_BEST_FRIENDS = 3


@register.simple_tag
def favorite_courses():
    return Friend.objects.filter(favorite_course__isnull=False) \
               .values('favorite_course__name') \
               .annotate(count=Count('favorite_course__name')) \
               .order_by('-count')[:AMOUNT_OF_FAVORITE_COURSES] \
        .values_list('favorite_course__name', flat=True)


@register.simple_tag
def all_aces():
    return Ace.objects.all()


@register.filter
def before_current_year(aces):
    return aces.filter(date__lt=_current_year_as_str()).count()


@register.filter
def before_current_year_tournaments(aces):
    return aces.filter(date__lt=_current_year_as_str(), type=Ace.TOURNAMENT).count()


@register.filter
def current_year(aces):
    return aces.filter(date__gte=_current_year_as_str()).count()


@register.filter
def current_year_tournaments(aces):
    return aces.filter(date__gte=_current_year_as_str(), type=Ace.TOURNAMENT).count()


@register.simple_tag
def favorite_discs(disc_type):
    return DiscInBag.objects.filter(type=disc_type) \
               .values('disc__display_name') \
               .annotate(count=Count('disc__display_name')) \
               .order_by('-count')[:AMOUNT_OF_FAVORITE_DISCS] \
        .values_list('disc__display_name', flat=True)


def _current_year_as_str():
    return datetime.now().strftime('%Y')


@register.filter
def order_by_rating(friends):
    return friends.order_by('-rating')[:AMOUNT_OF_BEST_FRIENDS]
