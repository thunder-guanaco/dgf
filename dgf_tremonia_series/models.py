from django.db import models
from django.db.models import Model
from django.utils.translation import gettext_lazy as _


class MetrixIds(Model):
    ids = models.CharField(_('IDs'), max_length=1000)

    def __str__(self):
        return str(self.ids)
