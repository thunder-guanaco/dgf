import logging
import re
from datetime import datetime

from django import template
from django.db.models import Count, Q

from ..models import Ace, DiscInBag, Course, Tournament, Result
from ..tremonia_series import DISC_GOLF_METRIX_TOURNAMENT_PAGE

register = template.Library()

AMOUNT_OF_FAVORITE_DISCS = 3
AMOUNT_OF_FAVORITE_COURSES = 3

logger = logging.getLogger(__name__)


@register.simple_tag
def favorite_courses():
    return Course.objects.all() \
               .annotate(count=Count('favorites')) \
               .filter(count__gte=1) \
               .order_by('-count')[:AMOUNT_OF_FAVORITE_COURSES]


@register.simple_tag
def all_aces():
    return Ace.objects.all()


@register.filter
def in_tournaments(aces):
    return aces.filter(type=Ace.TOURNAMENT)


@register.filter
def current_year(aces):
    return aces.filter(date__gte=_current_year_as_str())


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
def order_by(friends, ordering):
    attribute = ordering[1:] if ordering[0] == '-' else ordering
    query = Q(**{'%s__isnull' % attribute: False})
    return friends.filter(query).order_by(ordering)


@register.filter
def youtube_id(url):
    # full Youtube URL
    matches = re.findall('v=[a-zA-Z0-9_-]+', url)
    if matches:
        return matches[0].split('=')[1]

    # short Youtube URL
    matches = re.findall('youtu.be/[a-zA-Z0-9_-]+', url)
    if matches:
        return matches[0].split('/')[1]

    logger.warning(f'{url} is not a valid Youtube URL')
    return None


@register.filter
def filter_discs(friend, type):
    return list(filter(lambda disc: disc.type == type, friend.discs.all()))


@register.filter
def filter_by_type(queryset, type):
    return list(filter(lambda x: x.type == type, queryset))


@register.filter
def first_by_type(queryset, type):
    try:
        return filter_by_type(queryset, type)[0]
    except IndexError:
        return None


@register.simple_tag
def all_tournaments():
    return Tournament.objects.annotate(players_count=Count('attendance')) \
        .filter(begin__gte=datetime.now(),
                attendance__friend__is_active=True,
                players_count__gt=0) \
        .order_by('begin')


@register.filter
def attends(tournament, friend):
    return tournament.attendance.filter(friend=friend).exists()


@register.filter
def active(attendance):
    return attendance.filter(friend__is_active=True)


@register.simple_tag
def problematic_tournaments():
    return [tournament for tournament in Tournament.objects.all() if not tournament.first_positions_are_ok]


@register.filter
def podium_results(friend):
    return Result.objects.filter(friend=friend, position__in=[1, 2, 3]).order_by('tournament__begin')


@register.filter
def now_playing(friend):
    return Tournament.objects.filter(attendance__friend=friend, begin=datetime.today())


@register.filter
def next_tournaments(friend):
    return Tournament.objects.filter(attendance__friend=friend, begin__gt=datetime.now()).order_by('begin')


@register.filter
def metrix_url(tournament):
    return DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(tournament.metrix_id)
