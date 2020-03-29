import logging

from cms.models import User, CMSPlugin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.text import slugify

logger = logging.getLogger(__name__)


class Friend(User):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['slug'], name='unique_slug'),
        ]

    pdga_number = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    main_photo = models.ImageField(null=True, blank=True)

    nickname = models.CharField(max_length=30, null=True, blank=True)
    slug = models.SlugField(max_length=30, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, validators=[
        MaxValueValidator(2000),
        MinValueValidator(0)
    ])

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


class FriendPluginModel(CMSPlugin):
    friend = models.ForeignKey(Friend, on_delete=CASCADE)

    def __str__(self):
        return str(self.friend)
