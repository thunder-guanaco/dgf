import logging

from cms.models import CMSPlugin
from django.db import models
from django.db.models.deletion import CASCADE

from dgf.models import Friend, Course, Tour, Division

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

