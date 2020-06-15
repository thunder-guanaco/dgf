from django.test import TestCase

from .utils import create_friends
from ...models import Friend
from ...templatetags import dgf


class TemplatetagsBestPlayersTest(TestCase):

    def setUp(self):
        Friend.objects.all().delete()

    def test_best_players(self):
        manolo, kevin, fede, mario = create_friends(['manolo', 'kevin', 'fede', 'mario'],
                                                    ratings=[883, 1007, 903, 881])
        all_friends = Friend.objects.all()
        self.assertListEqual(list(dgf.order_by(all_friends, '-rating')), [kevin, fede, manolo])

    def test_best_players_someone_without_rating(self):
        manolo, kevin, wolfgang = create_friends(['manolo', 'kevin', 'wolfgang'],
                                                 ratings=[883, 1007, None])
        all_friends = Friend.objects.all()
        self.assertListEqual(list(dgf.order_by(all_friends, '-rating')), [kevin, manolo, wolfgang])

    def test_best_players_only_not_enough(self):
        manolo, kevin = create_friends(['manolo', 'kevin'],
                                       ratings=[883, 1007])
        all_friends = Friend.objects.all()
        self.assertListEqual(list(dgf.order_by(all_friends, '-rating')), [kevin, manolo])

    def test_best_players_without_friends(self):
        all_friends = Friend.objects.all()
        self.assertListEqual(list(dgf.order_by(all_friends, '-rating')), [])
