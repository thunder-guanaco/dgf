from django.db import models
from django.db.models import Model
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _

from dgf.models import Friend


class Team(Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_team_name'),
        ]

    name = models.CharField(_('Name'), max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Team {self.name}: (created {self.created})'


class TeamMembership(Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['team', 'friend'], name='friends can not belong to more than one team'),
        ]

    team = models.ForeignKey(Team, on_delete=CASCADE, related_name='members', verbose_name=_('Team'))
    friend = models.ForeignKey(Friend, on_delete=CASCADE, related_name='memberships', verbose_name=_('Friend'))

    def __str__(self):
        return f'{self.friend} belongs to team {self.team}'
