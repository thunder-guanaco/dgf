from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Model
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _

from dgf.models import Friend

POINTS_PER_MATCH = 10


class Team(Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_team_name'),
        ]

    name = models.CharField(_('Name'), max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    actor = models.ForeignKey(Friend, on_delete=CASCADE, related_name='created_teams', verbose_name=_('Actor'))

    @property
    def member_names(self):
        return " + ".join([membership.friend.short_name for membership in self.members.all()])

    def __str__(self):
        return f'{self.name} ({self.member_names})'


class TeamMembership(Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['friend'], name='only_one_team_per_friend'),
        ]

    team = models.ForeignKey(Team, on_delete=CASCADE, related_name='members', verbose_name=_('Team'))
    friend = models.ForeignKey(Friend, on_delete=CASCADE, related_name='memberships', verbose_name=_('Friend'))

    def __str__(self):
        return f'{self.friend} belongs to team {self.team}'


class Match(Model):
    class Meta:
        verbose_name_plural = "Matches"

    date = models.DateTimeField(auto_now_add=True)
    actor = models.ForeignKey(Friend, on_delete=CASCADE, related_name='created_matches', verbose_name=_('Actor'))

    def results_as_str(self):
        return " / ".join([f'{result.team.name}: {result.points}' for result in self.results.all()])

    results_as_str.short_description = 'Results'

    def __str__(self):
        return f'Match occurred at {self.date}'


class Result(Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['match', 'team'], name='teams_can_not_play_against_themselves'),
        ]

    match = models.ForeignKey(Match, on_delete=CASCADE, related_name='results', verbose_name=_('Match'))
    team = models.ForeignKey(Team, on_delete=CASCADE, related_name='results', verbose_name=_('Team'))
    points = models.PositiveIntegerField(_('Points'), validators=[MinValueValidator(0),
                                                                  MaxValueValidator(POINTS_PER_MATCH)])

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
