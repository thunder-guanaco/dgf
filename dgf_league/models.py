from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Model
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _

from dgf.models import Friend

POINTS_PER_MATCH = 10


def first_league_year():
    try:
        return Team.objects.earliest('created').year
    except Team.DoesNotExist:
        return None


class Team(Model):
    name = models.CharField(_('Name'), max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    actor = models.ForeignKey(Friend, on_delete=CASCADE, related_name='created_teams', verbose_name=_('Actor'))

    @property
    def member_names(self):
        return " + ".join([membership.friend.short_name for membership in self.members.all()])

    @property
    def year(self):
        return self.created.year

    def save(self, *args, **kwargs):
        self.created = datetime.now()
        if Team.objects.filter(name=self.name, created__year=self.created.year).exists():
            raise ValidationError(_(f'There\'s already a team with that name for the {self.created.year} league'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.member_names}) [{self.created.year}]'


class TeamMembership(Model):
    team = models.ForeignKey(Team, on_delete=CASCADE, related_name='members', verbose_name=_('Team'))
    friend = models.ForeignKey(Friend, on_delete=CASCADE, related_name='memberships', verbose_name=_('Friend'))

    def save(self, *args, **kwargs):
        membership = TeamMembership.objects.filter(friend=self.friend, team__created__year=self.team.created.year)
        if membership.exists():
            team = membership.get().team
            raise ValidationError(_(f'{self.friend} already belongs to the team "{team.name}" '
                                    f'for the {team.created.year} league'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.friend} belongs to team {self.team}'


class Match(Model):
    class Meta:
        verbose_name_plural = "Matches"

    created = models.DateTimeField(auto_now_add=True)
    actor = models.ForeignKey(Friend, on_delete=CASCADE, related_name='created_matches', verbose_name=_('Actor'))

    @property
    def year(self):
        return self.created.year

    def results_as_str(self):
        return " / ".join([f'{result.team.name}: {result.points}' for result in self.results.all()])

    results_as_str.short_description = 'Results'

    def __str__(self):
        return f'{self.results_as_str()} ({self.created})'


class Result(Model):
    match = models.ForeignKey(Match, on_delete=CASCADE, related_name='results', verbose_name=_('Match'))
    team = models.ForeignKey(Team, on_delete=CASCADE, related_name='results', verbose_name=_('Team'))
    points = models.PositiveIntegerField(_('Points'), validators=[MinValueValidator(0),
                                                                  MaxValueValidator(POINTS_PER_MATCH)])

    def save(self, *args, **kwargs):
        if Result.objects.filter(match__created__year=self.match.created.year, team=self.team).exists():
            raise ValidationError(_(f'There\'s already a result for {self.team} '
                                    f'for the {self.match.created.year} league'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.team} got {self.points} in a match'


class FriendWithoutTeam(Model):
    class Meta:
        verbose_name_plural = "Friends without team"
        constraints = [
            models.UniqueConstraint(fields=['friend'], name='friend_can_only_search_for_team_once'),
        ]

    friend = models.ForeignKey(Friend, on_delete=CASCADE, related_name='searching', verbose_name=_('Friend'))

    def __str__(self):
        return f'{self.friend} is searching for a team'
