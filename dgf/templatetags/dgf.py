import logging
import re
from datetime import datetime

from django import template
from django.db.models import Count, Max, Q, Sum

from dgf_cms.settings import DISC_GOLF_METRIX_TOURNAMENT_PAGE
from ..models import Ace, DiscInBag, Course, Tournament, Result, Friend

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
    if url is None:
        raise ValueError()

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
def tournaments_ending_today_with_metrix_id():
    return Tournament.objects.annotate(players_count=Count('attendance')) \
        .filter(metrix_id__isnull=False,
                end=datetime.today(),
                attendance__friend__is_active=True,
                players_count__gt=0) \
        .order_by('begin', 'end', 'name')


@register.simple_tag
def friends_podium_tournaments():
    return Tournament.objects.annotate(results_count=Count("results")) \
        .filter(results__position__in=[1, 2, 3]) \
        .order_by("-begin", "end", "name")


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
    return tournament.attendance.filter(friend__is_active=True)


@register.filter
def active_podium_results(tournament):
    return tournament.results.filter(friend__is_active=True, position__in=[1, 2, 3]).order_by('-position')


@register.simple_tag
def problematic_tournaments():
    return [tournament for tournament in Tournament.objects.filter(name__startswith='Tremonia Series') if
            not tournament.first_positions_are_ok]


@register.filter
def now_playing(friend):
    return Tournament.objects.filter(attendance__friend=friend,
                                     begin__lte=datetime.today(),
                                     end__gte=datetime.today())


@register.filter
def podium_results(friend):
    return Result.objects.filter(friend=friend, position__in=[1, 2, 3]).order_by('-tournament__begin')


@register.filter
def next_tournaments(friend):
    return Tournament.objects.filter(attendance__friend=friend, begin__gt=datetime.today()) \
        .order_by('begin', 'end', 'name')


@register.filter
def metrix_url(tournament):
    if tournament.metrix_id:
        return DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(tournament.metrix_id)
    else:
        return ''


@register.filter
def ts_number_mobile(tournament):
    return ts_number(tournament, mobile=True)


@register.filter
def ts_number(tournament, mobile=False):
    matches = re.findall(r'#\d+', tournament.name)
    if not matches:
        logger.warning(f'Tournament {tournament} has no fitting name for a Tremonia Series tournament')
        return ''
    return f'{matches[0]}' if mobile else f'TS{matches[0]}'


@register.filter
def all_results(tour):
    queryset = Result.objects.filter(tournament__tours=tour).values('friend')
    for tournament in tour.tournaments.all():
        # This SUM contains actually JUST ONE element(the result of the Friend for the given Tournament)
        queryset = queryset.annotate(**{f'points_{tournament.id}': Sum('points', filter=Q(tournament=tournament))}) \
                           .annotate(**{f'position_{tournament.id}': Sum('position', filter=Q(tournament=tournament))})
    return queryset


@register.filter
def players_count(tour):
    return dict(
        tour.tournaments.annotate(players_count=Max('results__position'))
            .filter(players_count__isnull=False)
            .values_list('id', 'players_count')
    )


@register.filter
def only_friends(results):
    friend_ids = [result['friend'] for result in results]
    return Friend.all_objects.filter(id__in=friend_ids)


@register.filter
def get_friend(friends, friend_id):
    return friends[friend_id]


@register.filter
def get_result(result, tournament):
    result = result.get(f'points_{tournament.id}')
    return result if result else '-'


@register.simple_tag
def all_friends():
    return Friend.objects.all()


@register.filter
def with_metrix_user_id(friends):
    return friends.filter(metrix_user_id__isnull=False)


@register.filter
def values(friends, fields):
    return friends.values(*fields.split(','))


@register.filter
def values_list(friends, fields):
    return friends.values_list(*fields.split(','))


@register.filter
def values_list_flat(friends, field):
    return friends.values_list(field, flat=True)


@register.filter
def to_list(queryset):
    return list(queryset)


@register.filter
def to_dict(queryset):
    return dict(queryset)
