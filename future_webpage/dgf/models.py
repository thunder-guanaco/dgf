import logging
import re
from decimal import Decimal

from cms.models import User, CMSPlugin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Model
from django.db.models.deletion import CASCADE, SET_NULL
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from partial_date import PartialDateField

from .post_actions import feedback_post_save

logger = logging.getLogger(__name__)

MAX_AMOUNT_OF_HIGHLIGHTS = 5


class Division(Model):
    """
    This needs to be filled with content from the PDGA:
    https://www.pdga.com/pdga-documents/tour-documents/divisions-ratings-and-points-factors
    """

    id = models.CharField(max_length=10, primary_key=True)
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text


class Course(Model):
    """
    This needs to be filled with content. Initially we provided a fixture (courses_de.json)
    If needed, more models will be added via django admin
    """

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'postal_code', 'country'], name='unique_course'),
        ]

    name = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    country = CountryField()

    def __str__(self):
        if self.city in self.name:
            if self.country == 'DE':
                place = ''
            else:
                place = ' ({})'.format(self.country)
        else:
            if self.country == 'DE':
                place = ' ({})'.format(self.city)
            else:
                place = ' ({}, {})'.format(self.city, self.country)

        return '{}{}'.format(self.name, place)


class Friend(User):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['slug'], name='unique_slug'),
        ]

    nickname = models.CharField(max_length=30, null=True, blank=True)
    club_role = models.CharField(max_length=200, null=True, blank=True)

    sponsor = models.CharField(max_length=200, null=True, blank=True)
    sponsor_logo = models.ImageField(null=True, blank=True)
    sponsor_link = models.URLField(null=True, blank=True)

    pdga_number = models.PositiveIntegerField(null=True, blank=True)
    division = models.ForeignKey(Division, null=True, blank=True, on_delete=SET_NULL)
    city = models.CharField(max_length=100, null=True, blank=True)
    main_photo = models.ImageField(null=True, blank=True)
    plays_since = models.PositiveIntegerField(null=True, blank=True,
                                              validators=[MinValueValidator(1926)])
    free_text = models.TextField(null=True, blank=True)
    favorite_course = models.ForeignKey(Course, null=True, blank=True, on_delete=SET_NULL)

    slug = models.SlugField(max_length=30, null=True, blank=True)
    rating = models.PositiveIntegerField(null=True, blank=True, validators=[
        MaxValueValidator(2000)
    ])
    total_tournaments = models.PositiveIntegerField(null=True, blank=True, default=0)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))

    @property
    def full_name(self):
        nickname = ' ({})'.format(self.nickname) if self.nickname else ''
        return '{} {}{}'.format(self.first_name, self.last_name, nickname)

    @property
    def short_name(self):
        return self.nickname or self.first_name

    @property
    def initials(self):
        return '{} {}'.format(self.first_name[0] if self.first_name else '',
                              self.last_name[0] if self.last_name else '')

    @property
    def putters(self):
        return self.discs.filter(type=DiscInBag.PUTTER)

    def mid_ranges(self):
        return self.discs.filter(type=DiscInBag.MID_RANGE)

    @property
    def fairway_drivers(self):
        return self.discs.filter(type=DiscInBag.FAIRWAY_DRIVER)

    @property
    def distance_drivers(self):
        return self.discs.filter(type=DiscInBag.DISTANCE_DRIVER)

    @property
    def in_the_bag_video(self):
        return self.videos.filter(type=Video.IN_THE_BAG).first()

    @property
    def ace_video(self):
        return self.videos.filter(type=Video.ACE).first()

    @property
    def other_videos(self):
        return self.videos.filter(type=Video.OTHER)

    def __str__(self):
        pdga_number = ' #{}'.format(self.pdga_number) if self.pdga_number else ''
        return '{} {}{}'.format(self.first_name, self.last_name, pdga_number)

    def save(self, *args, **kwargs):
        new_slug = self.slug or self.nickname or self.first_name or self.username
        self.slug = slugify(new_slug).lower()
        logger.info('Setting slug for {} to {}'.format(self.username, self.slug))
        super(Friend, self).save(*args, **kwargs)


class Feedback(Model):
    title = models.CharField(max_length=200)
    feedback = models.TextField()
    friend = models.ForeignKey(Friend, null=True, on_delete=CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.friend.short_name if self.friend else None, self.title)

    def save(self, *args, **kwargs):
        super(Feedback, self).save(*args, **kwargs)
        try:
            feedback_post_save(self)
        except:
            logger.warning('I could not create this feedback as an issue in Github!')


class Highlight(Model):
    content = models.CharField(max_length=100)
    friend = models.ForeignKey(Friend, on_delete=CASCADE, related_name='highlights')


class FriendPluginModel(CMSPlugin):
    friend = models.ForeignKey(Friend, on_delete=CASCADE)

    def __str__(self):
        return str(self.friend)


class Disc(models.Model):
    manufacturer = models.CharField(max_length=200, null=True, blank=True)
    mold = models.CharField(max_length=200, unique=True)
    display_name = models.CharField(max_length=200)

    def __str__(self):
        return '{} [{}]'.format(self.mold, self.manufacturer)

    def save(self, *args, **kwargs):
        self.display_name = re.sub(' *\(.*\)', '', self.mold)
        super(Disc, self).save(*args, **kwargs)


class DiscInBag(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['disc', 'friend'], name='unique_disc_for_friend'),
        ]

    PUTTER = 'P'
    MID_RANGE = 'M'
    FAIRWAY_DRIVER = 'F'
    DISTANCE_DRIVER = 'D'
    TYPE_CHOICES = (
        (PUTTER, _('Putter')),
        (MID_RANGE, _('Mid-range')),
        (FAIRWAY_DRIVER, _('Fairway driver')),
        (DISTANCE_DRIVER, _('Distance driver')),
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    amount = models.PositiveIntegerField(default=1)
    disc = models.ForeignKey(Disc, on_delete=CASCADE)
    friend = models.ForeignKey(Friend, on_delete=CASCADE, related_name='discs')

    @property
    def in_the_bag(self):
        count = '' if self.amount == 1 else '{}x '.format(self.amount)
        return '{}{}'.format(count, self.disc.display_name)

    def __str__(self):
        return '{}x {} ({})'.format(self.amount, self.disc.mold, self.get_type_display())


class Ace(models.Model):
    PRACTICE = 'P'
    CASUAL_ROUND = 'C'
    TOURNAMENT = 'T'
    TYPE_CHOICES = (
        (PRACTICE, _('Practice')),
        (CASUAL_ROUND, _('Casual Round')),
        (TOURNAMENT, _('Tournament')),
    )
    friend = models.ForeignKey(Friend, on_delete=CASCADE, related_name='aces')
    disc = models.ForeignKey(Disc, null=True, on_delete=SET_NULL)
    course = models.ForeignKey(Course, null=True, on_delete=SET_NULL)
    hole = models.CharField(max_length=20)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    date = PartialDateField(null=True, blank=True)

    def __str__(self):
        return '{} - {} {} {} {} [{}]'.format(self.course,
                                              _('Hole'), self.hole,
                                              _('with a'), self.disc.display_name,
                                              self.get_type_display(),
                                              " - {}".format(self.date) if self.date else "")


class Video(Model):

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['url', 'friend'], name='unique_video_for_friend'),
        ]

    IN_THE_BAG = 'B'
    ACE = 'A'
    OTHER = 'O'
    TYPE_CHOICES = (
        (IN_THE_BAG, _('In the bag')),
        (ACE, _('Ace')),
        (OTHER, _('Other')),
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=OTHER)
    url = models.URLField()
    friend = models.ForeignKey(Friend, on_delete=CASCADE, related_name='videos')

    @property
    def youtube_id(self):

        # full Youtube URL
        matches = re.findall('v=[a-zA-Z0-9_-]+', str(self.url))
        if matches:
            return matches[0].split('=')[1]

        # short Youtube URL
        matches = re.findall('youtu.be/[a-zA-Z0-9_-]+', str(self.url))
        if matches:
            return matches[0].split('/')[1]

        logger.warning('{} is not a valid Youtube URL'.format(self.url))
        return None

    def __str__(self):
        return str(self.url)
