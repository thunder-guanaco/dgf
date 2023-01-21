import logging

from django import template

from dgf_league.models import Team

register = template.Library()

logger = logging.getLogger(__name__)


@register.filter
def all_rival_teams(friend):
    return Team.objects.exclude(members__friend=friend)


@register.filter
def team_name(friend):
    return Team.objects.get(members__friend=friend).name
