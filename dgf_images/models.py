from django.db import models
from django.db.models import Model
from django.utils.translation import gettext_lazy as _


class ImageGenerator(Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['slug'], name='unique_image_generator_slug'),
        ]

    name = models.CharField(_('Name'), max_length=50, null=False, blank=False)
    slug = models.SlugField(_('Slug'), max_length=50, null=False, blank=False)
    active = models.BooleanField(_('Active'), null=False, blank=False, default=True)

    def __str__(self):
        return f'{self.name} (/{self.slug}) [{"active" if self.active else "inactive"}]'