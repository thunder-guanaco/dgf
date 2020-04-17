import logging
from decimal import Decimal

from cms.models import User, CMSPlugin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Model
from django.db.models.deletion import CASCADE
from django.utils.text import slugify

logger = logging.getLogger(__name__)

MAX_AMOUNT_OF_HIGHLIGHTS = 5


class Division(Model):
    """
    This needs to be filled with content from the PDGA:
    https://www.pdga.com/pdga-documents/tour-documents/divisions-ratings-and-points-factors
    """

    id = models.CharField(max_length=10, null=False, blank=False, primary_key=True)
    text = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.text


class Friend(User):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['slug'], name='unique_slug'),
        ]

    pdga_number = models.PositiveIntegerField(null=True, blank=True)
    division = models.ForeignKey(Division, null=True, on_delete=models.SET_NULL)
    city = models.CharField(max_length=100, null=True, blank=True)
    main_photo = models.ImageField(null=True, blank=True)
    plays_since = models.PositiveIntegerField(null=True, blank=True,
                                              validators=[MinValueValidator(1926)])
    free_text = models.TextField(null=True, blank=True)

    nickname = models.CharField(max_length=30, null=True, blank=True)
    slug = models.SlugField(max_length=30, null=True, blank=True)
    rating = models.PositiveIntegerField(null=True, blank=True, validators=[
        MaxValueValidator(2000)
    ])
    total_tournaments = models.PositiveIntegerField(null=True, blank=True, default=0)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))

    @property
    def initials(self):
        return '{} {}'.format(self.first_name[0] if self.first_name else '',
                              self.last_name[0] if self.last_name else '')

    def __str__(self):
        pdga_number = '#{}'.format(self.pdga_number) if self.pdga_number else ''
        return '{} {}{}'.format(self.first_name, self.last_name, pdga_number)

    def save(self, *args, **kwargs):
        new_slug = self.slug or self.nickname or self.first_name or self.username
        self.slug = slugify(new_slug).lower()
        logger.info('Setting slug for {} to {}'.format(self.username, self.slug))
        super(Friend, self).save(*args, **kwargs)


class Highlight(Model):
    content = models.CharField(max_length=100, null=False, blank=False)
    friend = models.ForeignKey(Friend, on_delete=CASCADE)


class FriendPluginModel(CMSPlugin):
    friend = models.ForeignKey(Friend, on_delete=CASCADE)

    def __str__(self):
        return str(self.friend)


class Disc(models.Model):
    manufacturer = models.CharField(max_length=200, null=True, blank=True)
    mold = models.CharField(max_length=200, null=True, blank=True, unique=True)
