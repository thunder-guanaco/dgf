import logging

from cms.models import CMSPlugin
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _

from dgf.models import Friend, Course, Tour, Tournament, Division

logger = logging.getLogger(__name__)


class CoursePluginModel(CMSPlugin):
    course = models.ForeignKey(Course, on_delete=CASCADE)

    def __str__(self):
        return f'Course plugin for {str(self.course)}'


class FriendPluginModel(CMSPlugin):
    friend = models.ForeignKey(Friend, on_delete=CASCADE)

    def __str__(self):
        return f'Friend plugin for {str(self.friend)}'


class TourPluginModel(CMSPlugin):
    tour = models.ForeignKey(Tour, on_delete=CASCADE)

    def __str__(self):
        return f'Tour plugin for {str(self.tour)}'


class HallOfFameType(models.TextChoices):
    TREMONIA_SERIES = 'ts', 'Tremonia Series'
    TREMONIA_PUTTING_LIGA = 'tpl', 'Tremonia Putting Liga'


class HallOfFamePluginModel(CMSPlugin):
    type = models.CharField(max_length=50, choices=HallOfFameType.choices)
    division = models.ForeignKey(Division, limit_choices_to={'id__in': ['MPO', 'MA4']},
                                 null=False, blank=False, on_delete=CASCADE)


class ResultsPluginModel(CMSPlugin):
    background_image = models.ImageField(_('Background image'), null=False, blank=False)
    width = models.CharField(_('Width'), max_length=6, null=False, blank=False, default="800px")
    height = models.CharField(_('Height'), max_length=6, blank=False, default="500px")


class ConcreteTournamentResultsPluginModel(ResultsPluginModel):
    tournament = models.ForeignKey(Tournament, on_delete=CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Concrete tournament result plugin for {self.tournament}\n' \
               f'with background image: {self.background_image}\n' \
               f'(width: {self.width}, height: {self.height})'


class LastTremoniaSeriesResultsPluginModel(ResultsPluginModel):

    def __str__(self):
        return f'Last Tremonia Series result plugin\n' \
               f'with background image: {self.background_image}\n' \
               f'(width: {self.width}, height: {self.height})'
