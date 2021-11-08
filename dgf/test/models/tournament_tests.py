from datetime import date

from django.test import TestCase

from dgf.models import Tournament


class TournamentModelTest(TestCase):

    def test_representation(self):
        self.assert_field('__str__', expected='Tremonia Series #24 (27. Jun 2021)',
                          name='Tremonia Series #24',
                          begin=date(day=27, month=6, year=2021),
                          end=date(day=27, month=6, year=2021),
                          url='http://discgolffriends.de/turniere/tremonia-series')

    def test_date(self):
        # same dates
        self.assert_field('date', expected='27. Jun 2021',
                          begin=date(day=27, month=6, year=2021), end=date(day=27, month=6, year=2021))

        # different days
        self.assert_field('date', expected='25. - 27. Jun 2021',
                          begin=date(day=25, month=6, year=2021), end=date(day=27, month=6, year=2021))

        # different months
        self.assert_field('date', expected='30. Jun - 01. Jul 2021',
                          begin=date(day=30, month=6, year=2021), end=date(day=1, month=7, year=2021))

    def assert_field(self, what, expected, **fields):
        Tournament.objects.all().delete()
        tournament = Tournament(**fields)
        tournament.save()
        actual = str(tournament) if what == '__str__' else getattr(tournament, what)
        self.assertEqual(actual, expected)
