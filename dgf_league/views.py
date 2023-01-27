from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from dgf_league.forms import AddResultForm, AddTeamForm
from dgf_league.models import Team, TeamMembership, Result, Match


class TeamIndexView(ListView):
    template_name = 'dgf/team_list.html'
    context_object_name = 'teams'
    queryset = Team.objects.all() \
        .annotate(played_matches=Count('results')) \
        .annotate(points=Coalesce(Sum('results__points'), 0)) \
        .order_by('-points', '-played_matches', 'created')


def one_more_value(data, key, value):
    updated_request = data.copy()
    updated_request[key] = str(value)
    return updated_request


@login_required
@require_POST
def team_add(request):
    actor = request.user.friend

    form = AddTeamForm(one_more_value(request.POST, 'actor', actor.id))
    if not form.is_valid():
        return HttpResponse(status=400, reason=form.errors_as_str())

    name = form.cleaned_data['name']
    partner = form.cleaned_data['partner']

    team = Team.objects.create(name=name, actor=actor)
    TeamMembership.objects.create(team=team, friend=actor)
    TeamMembership.objects.create(team=team, friend=partner)
    return HttpResponse(status=200)


@login_required
@require_POST
def result_add(request):
    actor = request.user.friend
    if not actor.memberships.count():
        return HttpResponse(status=400, reason=_('You don\'t have a team and therefore you can not add results'))

    own_team = actor.memberships.get().team

    form = AddResultForm(one_more_value(request.POST, 'own_team', own_team.id))
    if not form.is_valid():
        return HttpResponse(status=400, reason=form.errors_as_str())

    rival_team = form.cleaned_data['rival_team']
    own_points = form.cleaned_data['own_points']
    rival_points = form.cleaned_data['rival_points']

    existing_match = Match.objects.filter(results__team=own_team).filter(results__team=rival_team)
    if existing_match.exists():
        match = existing_match.get()
    else:
        match = Match.objects.create(actor=actor)

    Result.objects.update_or_create(match=match, team=own_team, defaults={'points': own_points})
    Result.objects.update_or_create(match=match, team=rival_team, defaults={'points': rival_points})

    return HttpResponse(status=200)
