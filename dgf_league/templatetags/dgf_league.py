import logging
from datetime import datetime

from django import template
from django.db.models import Count, Q

from dgf.models import Friend
from dgf.templatetags.dgf import calculate_real_positions
from dgf_league.models import Team, Match, first_league_year

register = template.Library()

logger = logging.getLogger(__name__)


@register.simple_tag
def all_league_years():
    return range(first_league_year(), datetime.today().year + 1)


@register.filter
def current_year(year):
    return year == datetime.today().year


def current_year_membership(friend):
    return friend.memberships.filter(team__created__year=datetime.today().year)


@register.filter
def current_year_membership_exists(friend):
    return current_year_membership(friend).exists()


@register.filter
def not_in(element, iterable):
    return element not in iterable


@register.filter
def all_friends_without_teams(year):
    return Friend.objects \
        .annotate(membership_count=Count('memberships', filter=Q(memberships__team__created__year=year))) \
        .filter(membership_count=0) \
        .order_by('first_name')


@register.filter
def all_rival_teams(friend, year):
    return Team.objects \
        .exclude(members__friend=friend) \
        .filter(created__year=year) \
        .annotate(against_me=Count('results', filter=Q(results__match__results__team__members__friend=friend))) \
        .filter(against_me=0) \
        .order_by('name')


@register.filter
def matches(year):
    return Match.objects.filter(created__year=year).order_by('created')


@register.filter
def all_team_matches(team):
    return Match.objects.filter(results__team=team).order_by('created')


@register.filter
def team_name(friend, year):
    return Team.objects.get(created__year=year, members__friend=friend).name


@register.simple_tag
def all_friends_without_team():
    return Friend.objects.exclude(searching=None)


@register.filter
def calculate_positions(teams):
    def set_position(team, position):
        team.position = position

    return calculate_real_positions(teams, lambda x: x.points, set_position)
