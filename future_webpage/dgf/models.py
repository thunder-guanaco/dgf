from django.db import models
from django.utils.text import slugify
from cms.models import User, CMSPlugin
from django.db.models.deletion import CASCADE
import logging

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

    @property
    def initials(self):
        return '{} {}'.format(self.first_name[0] if self.first_name else '',
                              self.last_name[0] if self.last_name else '')

    def __str__(self):
        pdga_number = '#{}'.format(self.pdga_number) if self.pdga_number else ''
        return '{} {}{}'.format(self.first_name, self.last_name, pdga_number)

    def save(self, *args, **kwargs):

        if self.slug:
            logger.info('Setting slug for {} to {} (slug field)'.format(self.username, self.slug))
            self.slug = self.slug.lower()

        else:
            if self.nickname:
                logger.info('Setting slug for {} to {} (nickname field)'.format(self.username, self.nickname))
                self.slug = slugify(self.nickname).lower()
            else:
                logger.info('Setting slug for {} to {} (first_name field)'.format(self.username, self.first_name))
                self.slug = slugify(self.first_name).lower()

        super(Friend, self).save(*args, **kwargs)


class FriendPluginModel(CMSPlugin):
    friend = models.ForeignKey(Friend, on_delete=CASCADE)

    def __str__(self):
        return str(self.friend)
