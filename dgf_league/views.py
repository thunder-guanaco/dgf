from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Sum, Count, F
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from dgf.models import Friend
from dgf_league.models import Team, TeamMembership, Result


class TeamIndexView(ListView):
    template_name = 'dgf/team_list.html'
    context_object_name = 'teams'
    queryset = Team.objects.all() \
        .annotate(points1=Coalesce(Sum('results_as_team_1__id'), 0)) \
        .annotate(points2=Coalesce(Sum('results_as_team_2__id'), 0)) \
        .annotate(points=F('points1') + F('points2')) \
        .annotate(played_matches1=Count('results_as_team_1')) \
        .annotate(played_matches2=Count('results_as_team_2')) \
        .annotate(played_matches=F('played_matches1') + F('played_matches2')) \
        .order_by('-points')
    # TODO check why Thunder Guanaco has more points and matches than it should


@login_required
@require_POST
def team_add(request):
    actor = request.user.friend

    name = request.POST.get('name')
    if not name:
        return HttpResponse(status=400, reason=_('Missing name'))

    partner_id = request.POST.get('partner')
    if not partner_id:
        return HttpResponse(status=400, reason=_('Missing partner'))

    if actor.id == int(partner_id):
        return HttpResponse(status=400, reason=_('You can not select yourself as partner'))

    try:
        partner = Friend.objects.get(id=partner_id)
    except Friend.DoesNotExist:
        return HttpResponse(status=400, reason=_(f'Friend with ID {partner_id} does not exist'))

    if partner.memberships.count() > 0:
        return HttpResponse(status=400, reason=_('The selected partner is already in another team'))

    team = Team.objects.create(name=name)
    TeamMembership.objects.create(team=team, friend=actor)
    TeamMembership.objects.create(team=team, friend=partner)

    return HttpResponse(status=200)


# TODO: it is time to start using django-rest-framework or something similar...
# I'm not proud of this and I will change it


@login_required
@require_POST
def result_add(request):
    actor = request.user.friend
    if not actor.memberships.count():
        return HttpResponse(status=400, reason=_(f'You don\'t have a team and therefore you can not add results'))

    team1 = actor.memberships.get().team

    team2 = request.POST.get('rival_team')
    if not team2:
        return HttpResponse(status=400, reason=_('Missing rival team'))
    team2 = Team.objects.get(id=team2)

    points1 = request.POST.get('own_team_points')
    if not points1:
        return HttpResponse(status=400, reason=_('Missing own team points'))

    points2 = request.POST.get('rival_team_points')
    if not points2:
        return HttpResponse(status=400, reason=_('Missing rival team points'))

    try:
        _, created = Result.objects.update_or_create(
            team1=team1,
            team2=team2,
            defaults={
                'points1': int(points1),
                'points2': int(points2)
            }
        )
        return HttpResponse(status=201 if created else 200)
    except ValidationError as error:
        return HttpResponse(status=400, reason=error.message)
