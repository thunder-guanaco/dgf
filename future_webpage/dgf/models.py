from django.db import models
from cms.models import User, CMSPlugin
from django.db.models.deletion import CASCADE


class Friend(User):

    pdga_number = models.IntegerField(null=True)
    city = models.CharField(max_length=100, null=True)
    main_photo = models.ImageField(null=True)

    def __str__(self):
        return '{} {} #{}'.format(self.first_name, self.last_name, self.pdga_number)


class FriendPluginModel(CMSPlugin):
    friend = models.ForeignKey(Friend, on_delete=CASCADE)

    def __str__(self):
        return str(self.friend)
