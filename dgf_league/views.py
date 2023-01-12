from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from dgf.models import Friend
from dgf_league.models import Team, TeamMembership


class TeamIndexView(ListView):
    template_name = 'dgf/team_list.html'
    context_object_name = 'teams'
    queryset = Team.objects.all()  # this will be extended: sorted by points


@login_required
@require_POST
def team_add(request):
    actor = request.user.friend

    partner_id = request.POST.get('partner')
    if not partner_id:
        return HttpResponse(status=400, reason=_('Missing partner'))

    name = request.POST.get('name')
    if not name:
        return HttpResponse(status=400, reason=_('Team name can not be empty'))

    try:
        with transaction.atomic():
            team = Team.objects.create(name=name)
            TeamMembership.objects.create(team=team, friend=actor)
            TeamMembership.objects.create(team=team, friend=Friend.objects.get(id=partner_id))
    except IntegrityError:
        return HttpResponse(status=400, reason='You can not select yourself as partner')

    return HttpResponse(status=200)
