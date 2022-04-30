from datetime import date

from django.test import TestCase

from dgf.models import Tournament, Tour, Division
from dgf.test.models.creator import create_divisions

IS_OK = True
NOT_OK = False


class TourModelTest(TestCase):

    def setUp(self):
        Tournament.objects.all().delete()
        Tour.objects.all().delete()
        create_divisions()

    def test_representation(self):
        self.assertEqual(str(Tour.objects.create(name='Tremonia Series 2022',
                                                 division=Division.objects.get(id='MPO'))),
                         'Tremonia Series 2022 (MPO - Pro Open)')

    def test_date_properties(self):
        tour = Tour.objects.create(name='test')
        first_tournament = Tournament.objects.create(name='first',
                                                     begin=date(day=1, month=1, year=1),
                                                     end=date(day=2, month=1, year=1))

        second_tournament = Tournament.objects.create(name='second',
                                                      begin=date(day=1, month=2, year=1),
                                                      end=date(day=2, month=2, year=1))

        third_tournament = Tournament.objects.create(name='second',
                                                     begin=date(day=1, month=2, year=1),
                                                     end=date(day=2, month=2, year=1))

        tour.tournaments.add(first_tournament)
        tour.tournaments.add(second_tournament)
        tour.tournaments.add(third_tournament)

        self.assertEqual(tour.begin, first_tournament.begin)
        self.assertEqual(tour.end, third_tournament.end)
