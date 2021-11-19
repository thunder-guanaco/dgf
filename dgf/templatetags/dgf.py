import logging
import re
from datetime import datetime

from django import template
from django.db.models import Count, Q, Sum

from ..models import Ace, DiscInBag, Course, Tournament, Result, Friend
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
    return aces.filter(date__gte=datetime.now().strftime('%Y'))


@register.simple_tag
def favorite_discs(disc_type):
    return DiscInBag.objects.filter(type=disc_type) \
               .values('disc__display_name') \
               .annotate(count=Count('disc__display_name')) \
               .order_by('-count')[:AMOUNT_OF_FAVORITE_DISCS] \
               .values_list('disc__display_name', flat=True)


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
def filter_by_type(queryset, type):
    return queryset.filter(type=type)


@register.simple_tag
def current_tournaments():
    return Tournament.objects.annotate(players_count=Count('attendance')) \
        .filter(begin__lte=datetime.today(),
                end__gte=datetime.today(),
                attendance__friend__is_active=True,
                players_count__gt=0) \
        .order_by('begin', 'end', 'name')


@register.simple_tag
def future_tournaments():
    return Tournament.objects.annotate(players_count=Count('attendance')) \
        .filter(begin__gt=datetime.today(),
                attendance__friend__is_active=True,
                players_count__gt=0) \
        .order_by('begin', 'end', 'name')


@register.filter
def attends(tournament, friend):
    return tournament.attendance.filter(friend=friend).exists()


@register.filter
def active_attendance(tournament):
    return tournament.attendance.all().filter(friend__is_active=True)


@register.simple_tag
def problematic_tournaments():
    return [tournament for tournament in Tournament.objects.all() if not tournament.first_positions_are_ok]


@register.filter
def podium_results(friend):
    return Result.objects.filter(friend=friend, position__in=[1, 2, 3]).order_by('tournament__begin')


@register.filter
def now_playing(friend):
    return Tournament.objects.filter(attendance__friend=friend,
                                     begin__lte=datetime.today(),
                                     end__gte=datetime.today())


@register.filter
def next_tournaments(friend):
    return Tournament.objects.filter(attendance__friend=friend, begin__gt=datetime.today())\
        .order_by('begin', 'end', 'name')


@register.filter
def metrix_url(tournament):
    if tournament.metrix_id:
        return DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(tournament.metrix_id)
    else:
        return ''


@register.filter
def ts_number(tournament):
    matches = re.findall(r'#\d+', tournament.name)
    if not matches:
        logger.warning(f'Tournament {tournament} has no fitting name for a Tremonia Series tournament')
        return ''
    return f'TS{matches[0]}'


def _best_results(result_dict, amount):
    tournament_points = [item for item in result_dict.items()
                         if item[1] is not None
                         and item[0] not in ['friend', 'total_points']]
    best_tournament_points = dict(sorted(tournament_points, key=lambda item: -item[1])[:amount])
    best_tournament_points['total_points'] = sum(best_tournament_points.values())
    best_tournament_points['friend'] = result_dict['friend']
    for key, value in result_dict.items():
        if key.startswith('position_'):
            best_tournament_points[key] = value
    return best_tournament_points


@register.filter
def best_results(tour, amount):
    queryset = Result.objects.filter(tournament__tour=tour).values('friend').annotate(total_points=Sum('points'))
    for tournament in tour.tournaments.all():
        queryset = queryset.annotate(**{f'points_{tournament.id}': Sum('points', filter=Q(tournament=tournament))})
        queryset = queryset.annotate(**{f'position_{tournament.id}': Sum('position', filter=Q(tournament=tournament))})

    best_results = [_best_results(result_dict, amount) for result_dict in queryset]
    return sorted(best_results, key=lambda item: -item['total_points'])


@register.filter
def all_friends(results):
    friend_ids = [result['friend'] for result in results]
    return {friend.id: friend for friend in Friend.all_objects.filter(id__in=friend_ids)}


@register.filter
def get_points_for(result_dict, tournament):
    result = result_dict.get(f'points_{tournament.id}')
    return result if result else '-'


@register.filter
def get_from_dict(list, key):
    return list[key]

