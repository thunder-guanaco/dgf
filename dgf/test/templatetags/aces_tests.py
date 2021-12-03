from datetime import datetime

from django.test import TestCase
from partial_date import PartialDate

from ...models import Course, Friend, Disc, Ace
from ...templatetags import dgf


class AcesTemplatetagsTest(TestCase):

    def setUp(self):
        Friend.objects.all().delete()
        Disc.objects.all().delete()
        Course.objects.all().delete()
        Ace.objects.all().delete()

    def test_all_aces(self):
        manolo = Friend.objects.create(username='manolo')
        fd = Disc.objects.create(mold='FD')
        wischlingen = Course.objects.create(name='Wischlingen')
        Ace.objects.create(friend=manolo, disc=fd, course=wischlingen, hole='5')
        self.assertEqual(dgf.all_aces().count(), 1)

    def test_all_aces_without_aces(self):
        self.assertEqual(dgf.all_aces().count(), 0)

    def test_aces_for_user(self):
        manolo = Friend.objects.create(username='manolo')
        fd = Disc.objects.create(mold='FD')
        wischlingen = Course.objects.create(name='Wischlingen')

        # before current year
        Ace.objects.create(friend=manolo, disc=fd, course=wischlingen, hole='5', type=Ace.TOURNAMENT,
                           date=PartialDate(f'{datetime.now().year - 2}-1-1'))
        Ace.objects.create(friend=manolo, disc=fd, course=wischlingen, hole='5', type=Ace.TOURNAMENT,
                           date=PartialDate(f'{datetime.now().year - 2}-2'))
        Ace.objects.create(friend=manolo, disc=fd, course=wischlingen, hole='5', type=Ace.CASUAL_ROUND,
                           date=PartialDate(f'{datetime.now().year - 2}'))
        Ace.objects.create(friend=manolo, disc=fd, course=wischlingen, hole='5', type=Ace.TOURNAMENT,
                           date=PartialDate(f'{datetime.now().year - 1}-6-7'))

        # current year
        Ace.objects.create(friend=manolo, disc=fd, course=wischlingen, hole='5', type=Ace.TOURNAMENT,
                           date=PartialDate(f'{datetime.now().year}-1-12'))
        Ace.objects.create(friend=manolo, disc=fd, course=wischlingen, hole='5', type=Ace.PRACTICE,
                           date=PartialDate(f'{datetime.now().year}'))

        self.assert_aces(manolo.aces, 4, 2, 1)

    def test_aces_for_all_users(self):
        manolo = Friend.objects.create(username='manolo')
        fede = Friend.objects.create(username='fede')
        fd = Disc.objects.create(mold='FD')
        wischlingen = Course.objects.create(name='Wischlingen')

        # before current year
        Ace.objects.create(friend=manolo, disc=fd, course=wischlingen, hole='5', type=Ace.TOURNAMENT,
                           date=PartialDate(f'{datetime.now().year - 2}-1-1'))
        Ace.objects.create(friend=fede, disc=fd, course=wischlingen, hole='5', type=Ace.TOURNAMENT,
                           date=PartialDate(f'{datetime.now().year - 2}-2'))
        Ace.objects.create(friend=manolo, disc=fd, course=wischlingen, hole='5', type=Ace.CASUAL_ROUND,
                           date=PartialDate(f'{datetime.now().year - 2}'))
        Ace.objects.create(friend=fede, disc=fd, course=wischlingen, hole='5', type=Ace.TOURNAMENT,
                           date=PartialDate(f'{datetime.now().year - 1}-6-7'))

        # current year
        Ace.objects.create(friend=manolo, disc=fd, course=wischlingen, hole='5', type=Ace.TOURNAMENT,
                           date=PartialDate(f'{datetime.now().year}-1-12'))
        Ace.objects.create(friend=fede, disc=fd, course=wischlingen, hole='5', type=Ace.PRACTICE,
                           date=PartialDate(f'{datetime.now().year}'))

        self.assert_aces(dgf.all_aces(), 4, 2, 1)

    def test_aces_no_aces(self):
        Friend.objects.create(username='manolo')
        Friend.objects.create(username='fede')
        Disc.objects.create(mold='FD')
        Course.objects.create(name='Wischlingen')

        self.assert_aces(Ace.objects.all(), 0, 0, 0)

    def test_aces_no_users(self):
        self.assert_aces(Ace.objects.all(), 0, 0, 0)

    def assert_aces(self, aces, expected_total_in_tournaments, expected_current_year,
                    expected_current_year_in_tournaments):
        self.assertEqual(dgf.in_tournaments(aces).count(), expected_total_in_tournaments)
        self.assertEqual(dgf.current_year(aces).count(), expected_current_year)
        self.assertEqual(dgf.in_tournaments(dgf.current_year(aces)).count(), expected_current_year_in_tournaments)
        self.assertEqual(dgf.current_year(dgf.in_tournaments(aces)).count(), expected_current_year_in_tournaments)
