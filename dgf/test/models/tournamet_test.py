from datetime import date

from django.test import TestCase

from dgf.models import Tournament, Result, Tour
from dgf.test.models.creator import create_friends, create_tournaments

IS_OK = True
NOT_OK = False


class TournamentModelTest(TestCase):

    def setUp(self):
        Tournament.objects.all().delete()
        Tour.objects.all().delete()

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

    def test_repeated_first_positions(self):
        tournament = create_tournaments(1)
        friends = create_friends(4)
        self.assert_that(tournament, IS_OK, friends, in_positions=[])  # empty results
        self.assert_that(tournament, IS_OK, friends, in_positions=[1, 2, 3, 4])
        self.assert_that(tournament, NOT_OK, friends, in_positions=[1, 2, 3, 3])
        self.assert_that(tournament, NOT_OK, friends, in_positions=[1, 2, 2, 3])
        self.assert_that(tournament, NOT_OK, friends, in_positions=[1, 2, 2, 4])
        self.assert_that(tournament, NOT_OK, friends, in_positions=[1, 2, 2, 2])
        self.assert_that(tournament, NOT_OK, friends, in_positions=[1, 1, 3, 4])
        self.assert_that(tournament, NOT_OK, friends, in_positions=[1, 1, 3, 3])
        self.assert_that(tournament, NOT_OK, friends, in_positions=[1, 1, 1, 2])
        self.assert_that(tournament, NOT_OK, friends, in_positions=[1, 1, 1, 3])
        self.assert_that(tournament, NOT_OK, friends, in_positions=[1, 1, 1, 4])
        self.assert_that(tournament, NOT_OK, friends, in_positions=[1, 1, 1, 1])

    def test_save_without_tour(self):
        friends = create_friends(2)
        tournament = create_tournaments(1)
        first = Result.objects.create(tournament=tournament,
                                      friend=friends[0],
                                      position=1)
        second = Result.objects.create(tournament=tournament,
                                       friend=friends[1],
                                       position=2)
        self.assertEqual(first.points, None)
        self.assertEqual(second.points, None)

        tournament.save()

        self.assertEqual(first.points, None)
        self.assertEqual(second.points, None)

    def test_save_with_tour(self):
        tour = Tour.objects.create(name='test', point_system=Tour.TS_POINTS_WITH_BEATEN_PLAYERS)
        friends = create_friends(2)
        tournament = create_tournaments(1)
        tournament.tour = tour
        tournament.save()
        first = Result.objects.create(tournament=tournament,
                                      friend=friends[0],
                                      position=1)
        second = Result.objects.create(tournament=tournament,
                                       friend=friends[1],
                                       position=2)
        self.assertEqual(first.points, None)
        self.assertEqual(second.points, None)

        tournament.save()
        first.refresh_from_db()
        second.refresh_from_db()

        self.assertEqual(first.points, 20)
        self.assertEqual(second.points, 17)

    def test_re_calculate_points_without_tour(self):
        friends = create_friends(2)
        tournament = create_tournaments(1)
        first = Result.objects.create(tournament=tournament,
                                      friend=friends[0],
                                      position=1)
        second = Result.objects.create(tournament=tournament,
                                       friend=friends[1],
                                       position=2)
        self.assertEqual(first.points, None)
        self.assertEqual(second.points, None)

        tournament.re_calculate_points()

        self.assertEqual(first.points, None)
        self.assertEqual(second.points, None)

    def test_re_calculate_points_with_tour(self):
        tour = Tour.objects.create(name='test', point_system=Tour.TS_POINTS_WITH_BEATEN_PLAYERS)
        friends = create_friends(2)
        tournament = create_tournaments(1)
        tournament.tour = tour
        tournament.save()
        first = Result.objects.create(tournament=tournament,
                                      friend=friends[0],
                                      position=1)
        second = Result.objects.create(tournament=tournament,
                                       friend=friends[1],
                                       position=2)
        self.assertEqual(first.points, None)
        self.assertEqual(second.points, None)

        tournament.re_calculate_points()
        first.refresh_from_db()
        second.refresh_from_db()

        self.assertEqual(first.points, 20)
        self.assertEqual(second.points, 17)

    def assert_that(self, tournament, ok, friends, in_positions):
        Result.objects.all().delete()
        self.create_result(tournament, friends, in_positions)

        nt = 'n\'t' if not ok else ''
        self.assertEqual(tournament.first_positions_are_ok, ok,
                         msg=f'Tournament with positions {in_positions} should{nt} be ok')

    def create_result(self, tournament, friends, positions):
        for i, position in enumerate(positions):
            Result.objects.create(tournament=tournament, friend=friends[i], position=position)
