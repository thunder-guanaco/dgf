from unittest import TestCase

from django.test import Client

from dgf.models import Friend


class ClientTest(TestCase):

    def setUp(self):
        Friend.objects.all().delete()
        self.friend, created = Friend.objects.get_or_create(username='friend')
        self.friend.set_password('12345')
        self.friend.bag_tag = 1
        self.friend.is_superuser = True
        self.friend.is_staff = True
        self.friend.save()

        self.client = Client()

    def login(self):
        self.client.login(username='friend', password='12345')
