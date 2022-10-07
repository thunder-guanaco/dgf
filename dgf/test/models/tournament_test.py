from datetime import date

from django.test import TestCase

from dgf.models import Tournament, Result, Tour
from dgf.test.models.creator import create_friends, create_tournaments
from dgf_cms.settings import GT_RESULTS_PAGE, PDGA_EVENT_URL, DISC_GOLF_METRIX_TOURNAMENT_PAGE

IS_OK = True
NOT_OK = False


class TournamentModelTest(TestCase):

    def setUp(self):
        Tournament.objects.all().delete()
        Tour.objects.all().delete()

    def test_representation(self):
        some_day = date(day=27, month=6, year=2021)

        self.assert_field('__str__', expected='Tremonia Series #24 (27. Jun. 2021)',
                          begin=some_day, end=some_day,
                          name='Tremonia Series #24')

        self.assert_field('__str__', expected='Tremonia Series #24 (27. Jun. 2021) [GT: 111]',
                          begin=some_day, end=some_day,
                          name='Tremonia Series #24', gt_id=111)
        self.assert_field('__str__', expected='Tremonia Series #24 (27. Jun. 2021) [PDGA: 222]',
                          begin=some_day, end=some_day,
                          name='Tremonia Series #24', pdga_id=222)
        self.assert_field('__str__', expected='Tremonia Series #24 (27. Jun. 2021) [Metrix: 333]',
                          begin=some_day, end=some_day,
                          name='Tremonia Series #24', metrix_id=333)

        self.assert_field('__str__', expected='Tremonia Series #24 (27. Jun. 2021) [GT: 111, PDGA: 222]',
                          begin=some_day, end=some_day,
                          name='Tremonia Series #24', gt_id=111, pdga_id=222)
        self.assert_field('__str__', expected='Tremonia Series #24 (27. Jun. 2021) [GT: 111, Metrix: 333]',
                          begin=some_day, end=some_day,
                          name='Tremonia Series #24', gt_id=111, metrix_id=333)
        self.assert_field('__str__', expected='Tremonia Series #24 (27. Jun. 2021) [PDGA: 222, Metrix: 333]',
                          begin=some_day, end=some_day,
                          name='Tremonia Series #24', pdga_id=222, metrix_id=333)

        self.assert_field('__str__', expected='Tremonia Series #24 (27. Jun. 2021) [GT: 111, PDGA: 222, Metrix: 333]',
                          begin=some_day, end=some_day,
                          name='Tremonia Series #24', gt_id=111, pdga_id=222, metrix_id=333)

    def test_date(self):
        # same dates
        self.assert_field('date', expected='27. Jun. 2021',
                          begin=date(day=27, month=6, year=2021), end=date(day=27, month=6, year=2021))

        # different days
        self.assert_field('date', expected='25. - 27. Jun. 2021',
                          begin=date(day=25, month=6, year=2021), end=date(day=27, month=6, year=2021))

        # different months
        self.assert_field('date', expected='30. Jun. - 01. Jul. 2021',
                          begin=date(day=30, month=6, year=2021), end=date(day=1, month=7, year=2021))

    def test_url(self):
        gt = GT_RESULTS_PAGE.format(111)
        pdga = PDGA_EVENT_URL.format(222)
        metrix = DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(333)

        self.assert_url(None)  # no external IDs

        self.assert_url(gt, gt_id=111)
        self.assert_url(None, gt_id=111, old=True)
        self.assert_url(pdga, pdga_id=222)
        self.assert_url(metrix, metrix_id=333)

        self.assert_url(gt, gt_id=111, pdga_id=222)
        self.assert_url(gt, gt_id=111, metrix_id=333)
        self.assert_url(pdga, gt_id=111, pdga_id=222, old=True)
        self.assert_url(metrix, gt_id=111, metrix_id=333, old=True)
        self.assert_url(pdga, pdga_id=222, metrix_id=333)

        self.assert_url(gt, gt_id=111, pdga_id=222, metrix_id=333)
        self.assert_url(pdga, gt_id=111, pdga_id=222, metrix_id=333, old=True)

    def assert_url(self, expected_url, gt_id=None, pdga_id=None, metrix_id=None, old=False):
        tournament_date = date.today() if not old else date(day=21, month=9, year=2008)
        self.assert_field('url', expected=expected_url,
                          gt_id=gt_id, pdga_id=pdga_id, metrix_id=metrix_id,
                          begin=tournament_date, end=tournament_date)

    def assert_field(self, what, expected, **fields):
        Tournament.objects.all().delete()
        tournament = Tournament(**fields)
        tournament.save()
        actual = str(tournament) if what == '__str__' else getattr(tournament, what)
        self.assertEqual(actual, expected)

    def test_repeated_first_positions(self):
        tournament = create_tournaments(1)
        tournament.name = 'Tremonia Series #1'
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

    def test_recalculate_points(self):
        friends = create_friends(2)
        tournament = create_tournaments(1)
        tournament.point_system = Tournament.TS_POINTS_WITH_BEATEN_PLAYERS
        tournament.save()
        first = Result.objects.create(tournament=tournament,
                                      friend=friends[0],
                                      position=1)
        second = Result.objects.create(tournament=tournament,
                                       friend=friends[1],
                                       position=2)
        self.assertEqual(first.points, None)
        self.assertEqual(second.points, None)

        tournament.recalculate_points()
        first.refresh_from_db()
        second.refresh_from_db()

        self.assertEqual(first.points, 20)
        self.assertEqual(second.points, 17)

    def test_recalculate_points_without_point_system(self):
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

        tournament.recalculate_points()
        first.refresh_from_db()
        second.refresh_from_db()

        self.assertEqual(first.points, None)
        self.assertEqual(second.points, None)

    def assert_that(self, tournament, ok, friends, in_positions):
        Result.objects.all().delete()
        self.create_result(tournament, friends, in_positions)

        nt = 'n\'t' if not ok else ''
        self.assertEqual(tournament.first_positions_are_ok, ok,
                         msg=f'Tournament with positions {in_positions} should{nt} be ok')

    def create_result(self, tournament, friends, positions):
        for i, position in enumerate(positions):
            Result.objects.create(tournament=tournament, friend=friends[i], position=position)
