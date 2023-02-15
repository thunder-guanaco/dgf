import logging

from django import template
from django.db.models import Count, Q

from dgf.models import Friend
from dgf_league.models import Team, Match

register = template.Library()

logger = logging.getLogger(__name__)


@register.simple_tag
def all_friends_without_teams():
    return Friend.objects.annotate(membership_count=Count('memberships')) \
        .filter(membership_count=0) \
        .order_by('first_name')


@register.filter
def all_rival_teams(friend):
    return Team.objects \
        .exclude(members__friend=friend) \
        .annotate(against_me=Count('results', filter=Q(results__match__results__team__members__friend=friend))) \
        .filter(against_me=0) \
        .order_by('name')


@register.simple_tag
def all_matches():
    return Match.objects.all().order_by('date')


@register.filter
def all_team_matches(team):
    return Match.objects.filter(results__team=team).order_by('date')


@register.filter
def team_name(friend):
    return Team.objects.get(members__friend=friend).name


@register.simple_tag
def all_friends_without_team():
    return Friend.objects.exclude(searching=None)


@register.filter
def calculate_positions(teams):
    last, rest = teams[0], teams[1:]
    last.position = 1

    for position, team in enumerate(rest, start=2):

        if team.points == last.points:
            team.position = last.position
        else:
            team.position = position

        last = team

    return teams
