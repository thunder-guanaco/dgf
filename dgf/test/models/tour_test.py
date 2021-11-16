from datetime import date

from django.test import TestCase

from dgf.models import Tournament, Result, Tour
from dgf.test.models.creator import create_friends, create_tournaments

IS_OK = True
NOT_OK = False


class TourModelTest(TestCase):

    def setUp(self):
        Tournament.objects.all().delete()
        Tour.objects.all().delete()

    def test_representation(self):
        self.assertEqual(str(Tour.objects.create(name='Tremonia Series 2022')), 'Tremonia Series 2022')

    def test_date_properties(self):
        tour = Tour.objects.create(name='test', point_system=Tour.TS_POINTS_WITH_BEATEN_PLAYERS)
        first_tournament = Tournament.objects.create(name='first', tour=tour,
                                                     begin=date(day=1, month=1, year=1),
                                                     end=date(day=2, month=1, year=1))
        second_tournament = Tournament.objects.create(name='second', tour=tour,
                                                      begin=date(day=1, month=2, year=1),
                                                      end=date(day=2, month=2, year=1))
        self.assertEqual(tour.begin, first_tournament.begin)
        self.assertEqual(tour.end, second_tournament.end)

    def test_save(self):
        tour = Tour.objects.create(name='test', point_system=Tour.TS_POINTS_WITH_BEATEN_PLAYERS)
        friends = create_friends(2)
        tournaments = create_tournaments(2)
        for tournament in tournaments:
            tournament.tour = tour
            tournament.save()
        first_tournament_first = Result.objects.create(tournament=tournaments[0],
                                                       friend=friends[0],
                                                       position=1)
        first_tournament_second = Result.objects.create(tournament=tournaments[0],
                                                        friend=friends[1],
                                                        position=2)
        second_tournament_first = Result.objects.create(tournament=tournaments[1],
                                                        friend=friends[0],
                                                        position=1)
        second_tournament_second = Result.objects.create(tournament=tournaments[1],
                                                         friend=friends[1],
                                                         position=2)

        self.assertEqual(first_tournament_first.points, None)
        self.assertEqual(first_tournament_second.points, None)
        self.assertEqual(second_tournament_first.points, None)
        self.assertEqual(second_tournament_second.points, None)

        tour.save()
        first_tournament_first.refresh_from_db()
        first_tournament_second.refresh_from_db()
        second_tournament_first.refresh_from_db()
        second_tournament_second.refresh_from_db()

        self.assertEqual(first_tournament_first.points, 20)
        self.assertEqual(first_tournament_second.points, 17)
        self.assertEqual(second_tournament_first.points, 20)
        self.assertEqual(second_tournament_second.points, 17)
