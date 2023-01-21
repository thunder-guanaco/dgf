from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
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

    @property
    def info(self):
        members = [membership.friend.short_name for membership in self.members.all()]
        return f'{self.name}: ({" + ".join(members)})'

    def __str__(self):
        return self.name


class TeamMembership(Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['friend'], name='only_one_team_per_friend'),
        ]

    team = models.ForeignKey(Team, on_delete=CASCADE, related_name='members', verbose_name=_('Team'))
    friend = models.ForeignKey(Friend, on_delete=CASCADE, related_name='memberships', verbose_name=_('Friend'))

    def __str__(self):
        return f'{self.friend} belongs to team {self.team}'


class Result(Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['team1', 'team2'], name='teams_only_play_once_against_each_other'),
        ]

    team1 = models.ForeignKey(Team, on_delete=CASCADE, related_name='results_as_team_1', verbose_name=_('Team 1'))
    team2 = models.ForeignKey(Team, on_delete=CASCADE, related_name='results_as_team_2', verbose_name=_('Team 2'))
    points1 = models.PositiveIntegerField(_('Points Team 1'), validators=[MinValueValidator(0), MaxValueValidator(5)])
    points2 = models.PositiveIntegerField(_('Points Team 2'), validators=[MinValueValidator(0), MaxValueValidator(5)])
    created = models.DateTimeField(auto_now_add=True)

    def clean(self, *args, **kwargs):
        if (self.points1 + self.points2) != 5:
            raise ValidationError(_('The sum of all points must be 5'))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.team1} {self.points1} - {self.points2} {self.team2}'
