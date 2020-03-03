from django.db import models
from cms.models import User, CMSPlugin
from django.db.models.deletion import CASCADE


class Friend(User):

    pdga_number = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    main_photo = models.ImageField(null=True, blank=True)

    @property
    def initials(self):
        return '{} {}'.format(self.first_name[0] if self.first_name else '',
                              self.last_name[0] if self.last_name else '')

    def __str__(self):
        return '{} {} {}'.format(self.first_name, self.last_name,
                                 '#{}'.format(self.pdga_number) if self.pdga_number else '')


class FriendPluginModel(CMSPlugin):
    friend = models.ForeignKey(Friend, on_delete=CASCADE)

    def __str__(self):
        return str(self.friend)
