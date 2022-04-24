from cookie_consent.models import CookieGroup, Cookie
from django.db import models
from django.utils.translation import gettext_lazy as _


class CookieGroupTranslation(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cookie_group', 'language'], name='unique_cookie_group_translation'),
        ]

    cookie_group = models.ForeignKey(CookieGroup, on_delete=models.CASCADE)
    language = models.CharField(_('Language'), max_length=32, blank=False, null=False)
    name = models.CharField(_('Name'), max_length=100, blank=False, null=False)
    description = models.TextField(_('Description'), blank=False, null=False)

    def __str__(self):
        return f'{self.cookie_group} ({self.language}): {self.name}, {self.description}'


class CookieTranslation(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cookie', 'language'], name='unique_cookie_translation'),
        ]

    cookie = models.ForeignKey(Cookie, on_delete=models.CASCADE)
    language = models.CharField(_('Language'), max_length=32, blank=False, null=False)
    description = models.TextField(_('Description'), blank=False, null=False)

    def __str__(self):
        return f'{self.cookie} ({self.language}): {self.description}'
