from datetime import date

import responses
from django.test import TestCase

from dgf.disc_golf_metrix.tremonia_series import TremoniaSeriesImporter
from dgf.models import Tournament, Friend, Attendance, Result, Tour, Division
from dgf.test.disc_golf_metrix.ts_responses import add_one_ts_tournament, add_five_ts_tournaments_for_tours, \
    add_three_ts_tournaments
from dgf.test.models.creator import create_divisions
from dgf_cms.settings import DISC_GOLF_METRIX_TOURNAMENT_PAGE


class TremoniaSeriesImportTest(TestCase):

    def setUp(self):
        Tournament.objects.all().delete()
        Tour.objects.all().delete()
        Friend.objects.all().delete()
        Division.objects.all().delete()
        create_divisions()

    @responses.activate
    def test_tournaments(self):
        add_three_ts_tournaments()
        TremoniaSeriesImporter().update_tournaments()

        tournaments = Tournament.objects.filter(name__startswith='Tremonia Series')
        self.assertEqual(tournaments.count(), 3)
        for id in [1, 2, 3]:
            self.assert_tournament(tournaments, id)

    @responses.activate
    def test_tournament_incomplete_tournament(self):
        Tournament.objects.create(metrix_id=12345,
                                  name='Tremonia Series #28',
                                  begin=date(year=1000, month=1, day=1),
                                  end=date(year=1000, month=1, day=1))
        add_one_ts_tournament(12345, 'Tremonia Series #28 (Putter)', '1000-01-01')

        TremoniaSeriesImporter().update_tournaments()

        tournament = Tournament.objects.get(metrix_id=12345)
        self.assertEqual(tournament.name, 'Tremonia Series #28 (Putter)')
        self.assertEqual(tournament.url, DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(12345))
        self.assertEqual(tournament.begin, date(year=1000, month=1, day=1))
        self.assertEqual(tournament.end, date(year=1000, month=1, day=1))

    @responses.activate
    def test_tournament_name_change(self):
        Tournament.objects.create(metrix_id=12345,
                                  name='Tremonia Series #28',
                                  begin=date(year=1000, month=1, day=1),
                                  end=date(year=1000, month=1, day=1))
        add_one_ts_tournament(12345, 'Tremonia Series #28 (Putter)', '1000-01-01')

        TremoniaSeriesImporter().update_tournaments()

        tournament = Tournament.objects.get(metrix_id=12345)
        self.assertEqual(tournament.name, 'Tremonia Series #28 (Putter)')
        self.assertEqual(tournament.url, DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(12345))
        self.assertEqual(tournament.begin, date(year=1000, month=1, day=1))
        self.assertEqual(tournament.end, date(year=1000, month=1, day=1))

    @responses.activate
    def test_tournament_date_change(self):
        Tournament.objects.create(metrix_id=12345,
                                  name='Tremonia Series #28',
                                  begin=date(year=1000, month=1, day=2),
                                  end=date(year=1000, month=1, day=3))
        add_one_ts_tournament(12345, 'Tremonia Series #28 (Putter)', '1000-01-01')

        TremoniaSeriesImporter().update_tournaments()

        tournament = Tournament.objects.get(metrix_id=12345)
        self.assertEqual(tournament.name, 'Tremonia Series #28 (Putter)')
        self.assertEqual(tournament.url, DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(12345))
        self.assertEqual(tournament.begin, date(year=1000, month=1, day=1))
        self.assertEqual(tournament.end, date(year=1000, month=1, day=1))

    @responses.activate
    def test_tournament_with_results(self):
        Friend.objects.create(username='manolo', first_name='Manolo', metrix_user_id='manolo')
        Friend.objects.create(username='fede', first_name='Federico', metrix_user_id='fede')
        add_one_ts_tournament(12345, 'Test', '1000-01-01', players=[('manolo', 1, ''), ('fede', 2, '')])

        TremoniaSeriesImporter().update_tournaments()

        tournament = Tournament.objects.get(metrix_id=12345)
        results = [(result.friend.username, result.position, result.division.id) for result in
                   tournament.results.all().order_by('position')]
        self.assertEqual(results, [('manolo', 1, 'MPO'), ('fede', 2, 'MPO')])

    @responses.activate
    def test_tournament_with_results_from_different_divisions(self):
        Friend.objects.create(username='manolo', first_name='Manolo', metrix_user_id='manolo')
        Friend.objects.create(username='david', first_name='David', metrix_user_id='david')
        Friend.objects.create(username='chris', first_name='Chris', metrix_user_id='chris')
        Friend.objects.create(username='marcel', first_name='Marcel', metrix_user_id='marcel')
        add_one_ts_tournament(12345, 'Test', '1000-01-01', players=[('manolo', 1, 'Open'),
                                                                    ('david', 2, 'Open'),
                                                                    ('chris', 3, 'Open'),
                                                                    ('jan', 1, 'Amateur'),
                                                                    ('anna', 2, 'Amateur'),
                                                                    ('marcel', 3, 'Amateur')])

        TremoniaSeriesImporter().update_tournaments()

        tournament = Tournament.objects.get(metrix_id=12345)
        results = [(result.friend.username, result.position, result.division.id) for result in
                   tournament.results.all().order_by('-division__id', 'position')]
        self.assertEqual(results, [('manolo', 1, 'MPO'), ('david', 2, 'MPO'), ('chris', 3, 'MPO'),
                                   ('jan', 1, 'MA4'), ('anna', 2, 'MA4'), ('marcel', 3, 'MA4')])

    @responses.activate
    def test_tournament_with_existing_results(self):
        tournament = Tournament.objects.create(metrix_id=12345,
                                               name='Test',
                                               begin=date(year=1000, month=1, day=1),
                                               end=date(year=1000, month=1, day=1))
        manolo = Friend.objects.create(username='manolo', first_name='Manolo', metrix_user_id='manolo')
        fede = Friend.objects.create(username='fede', first_name='Federico', metrix_user_id='fede')
        Result.objects.create(friend=manolo, tournament=tournament, position=2, division=Division.objects.get(id='MPO'))
        Result.objects.create(friend=fede, tournament=tournament, position=1, division=Division.objects.get(id='MPO'))
        add_one_ts_tournament(12345, 'Test', '1000-01-01', players=[('manolo', 1, ''), ('fede', 2, '')])

        TremoniaSeriesImporter().update_tournaments()

        tournament = Tournament.objects.get(metrix_id=12345)
        self.assertEqual(tournament.results.all().count(), 2)  # no results were added
        results = [(result.friend.username, result.position, result.division.id) for result in
                   tournament.results.all().order_by('position')]
        self.assertEqual(results, [('fede', 1, 'MPO'), ('manolo', 2, 'MPO')])

    @responses.activate
    def test_tournament_with_results_and_points(self):
        Friend.objects.create(username='manolo', first_name='Manolo', metrix_user_id='manolo')
        Friend.objects.create(username='fede', first_name='Federico', metrix_user_id='fede')
        add_one_ts_tournament(12345, 'Test', '1000-01-01', players=[('manolo', 1, ''), ('fede', 2, '')])

        TremoniaSeriesImporter().update_tournaments()

        tournament = Tournament.objects.get(metrix_id=12345)
        results = [(result.friend.username, result.position, result.division.id, result.points) for result in
                   tournament.results.all().order_by('position')]
        self.assertEqual(results, [('manolo', 1, 'MPO', 20), ('fede', 2, 'MPO', 17)])

    @responses.activate
    def test_tournament_with_results_in_other_format(self):
        Friend.objects.create(username='manolo', first_name='Manolo', metrix_user_id='manolo')
        Friend.objects.create(username='fede', first_name='Federico', metrix_user_id='fede')
        add_one_ts_tournament(12345, 'Test', '1000-01-01',
                              players=[('manolo', 1, ''), ('fede', 2, '')],
                              other_format=True)

        TremoniaSeriesImporter().update_tournaments()

        tournament = Tournament.objects.get(metrix_id=12345)
        results = [(result.friend.username, result.position, result.division.id) for result in
                   tournament.results.all().order_by('position')]
        self.assertEqual(results, [('manolo', 1, 'MPO'), ('fede', 2, 'MPO')])

    @responses.activate
    def test_tournament_with_attendance(self):
        Friend.objects.create(username='manolo', first_name='Manolo', metrix_user_id='manolo')
        Friend.objects.create(username='fede', first_name='Federico', metrix_user_id='fede')
        add_one_ts_tournament(12345, 'Test', '3000-01-01', players=[('manolo', None, ''), ('fede', None, '')])

        TremoniaSeriesImporter().update_tournaments()

        tournament = Tournament.objects.get(metrix_id=12345)
        attendance = set(tournament.attendance.all().values_list('friend__username', flat=True))
        self.assertEqual(attendance, {'manolo', 'fede'})

    @responses.activate
    def test_existing_tournament_with_attendance(self):
        Friend.objects.create(username='manolo', first_name='Manolo', metrix_user_id='manolo')
        Friend.objects.create(username='fede', first_name='Federico', metrix_user_id='fede')
        Tournament.objects.create(metrix_id=12345,
                                  name='Test',
                                  begin=date(year=3000, month=1, day=1),
                                  end=date(year=3000, month=1, day=1))
        add_one_ts_tournament(12345, 'Test', '3000-01-01', players=[('manolo', None, ''), ('fede', None, '')])

        TremoniaSeriesImporter().update_tournaments()

        tournament = Tournament.objects.get(metrix_id=12345)
        attendance = set(tournament.attendance.all().values_list('friend__username', flat=True))
        self.assertEqual(attendance, {'manolo', 'fede'})

    @responses.activate
    def test_existing_tournament_adding_attendance(self):
        manolo = Friend.objects.create(username='manolo', first_name='Manolo', metrix_user_id='manolo')
        Friend.objects.create(username='fede', first_name='Federico', metrix_user_id='fede')
        tournament = Tournament.objects.create(metrix_id=12345,
                                               name='Test',
                                               begin=date(year=3000, month=1, day=1),
                                               end=date(year=3000, month=1, day=1))
        Attendance.objects.create(tournament=tournament, friend=manolo)
        add_one_ts_tournament(12345, 'Test', '3000-01-01', players=[('manolo', None, ''), ('fede', None, '')])

        TremoniaSeriesImporter().update_tournaments()

        tournament = Tournament.objects.get(metrix_id=12345)
        attendance = set(tournament.attendance.all().values_list('friend__username', flat=True))
        self.assertEqual(attendance, {'manolo', 'fede'})

    @responses.activate
    def test_add_automatic_tours(self):
        Friend.objects.create(username='manolo', first_name='Manolo', metrix_user_id='manolo')
        Friend.objects.create(username='fede', first_name='Federico', metrix_user_id='fede')

        add_five_ts_tournaments_for_tours(players=[('manolo', 1, ''), ('fede', 2, '')])

        TremoniaSeriesImporter().update_tournaments()

        self.assert_tournament_in_tour('Ewige Tabelle', 'MPO', {1, 2, 3, 4}, expected_evaluate_how_many=10000)
        self.assert_tournament_in_tour('Tremonia Series 1000', 'MPO', {1, 2, 3}, expected_evaluate_how_many=7)
        self.assert_tournament_in_tour('Tremonia Series 2000', 'MPO', {4}, expected_evaluate_how_many=7)
        # tournament 5 doesn't have any results and therefore there are no divisions, and it won't be added

    @responses.activate
    def test_add_automatic_tours_with_existing_tours(self):
        Friend.objects.create(username='manolo', first_name='Manolo', metrix_user_id='manolo')
        Friend.objects.create(username='fede', first_name='Federico', metrix_user_id='fede')
        mpo, _ = Division.objects.get_or_create(id='MPO')
        default_tour = Tour.objects.create(name='Ewige Tabelle',
                                           division=mpo,
                                           evaluate_how_many=10000)
        tour_1000 = Tour.objects.create(name='Tremonia Series 1000',
                                        division=mpo,
                                        evaluate_how_many=7)
        ts1 = Tournament.objects.create(metrix_id=1,
                                        name='Tremonia Series #1',
                                        begin=date(year=1000, month=1, day=1),
                                        end=date(year=1000, month=1, day=1))
        Tournament.objects.create(metrix_id=2,
                                  name='Tremonia Series #2',
                                  begin=date(year=1000, month=2, day=2),
                                  end=date(year=1000, month=2, day=2))

        ts1.tours.add(default_tour)
        ts1.tours.add(tour_1000)

        add_five_ts_tournaments_for_tours(players=[('manolo', 1, ''), ('fede', 2, '')])

        TremoniaSeriesImporter().update_tournaments()

        self.assert_tournament_in_tour('Ewige Tabelle', 'MPO', {1, 2, 3, 4}, expected_evaluate_how_many=10000)
        self.assert_tournament_in_tour('Tremonia Series 1000', 'MPO', {1, 2, 3}, expected_evaluate_how_many=7)
        self.assert_tournament_in_tour('Tremonia Series 2000', 'MPO', {4}, expected_evaluate_how_many=7)
        # tournament 5 doesn't have any results and therefore there are no divisions, and it won't be added

    @responses.activate
    def test_add_automatic_tours_with_different_divisions(self):
        Friend.objects.create(username='manolo', first_name='Manolo', metrix_user_id='manolo')
        Friend.objects.create(username='fede', first_name='Federico', metrix_user_id='fede')
        Tournament.objects.create(metrix_id=1,
                                  name='Tremonia Series #1',
                                  begin=date(year=1000, month=1, day=1),
                                  end=date(year=1000, month=1, day=1))
        Tournament.objects.create(metrix_id=2,
                                  name='Tremonia Series #2',
                                  begin=date(year=1000, month=2, day=2),
                                  end=date(year=1000, month=2, day=2))
        add_five_ts_tournaments_for_tours(players=[('manolo', 1, 'Open'), ('fede', 2, 'Amateur')])

        TremoniaSeriesImporter().update_tournaments()

        self.assert_tournament_in_tour('Ewige Tabelle', 'MPO', {1, 2, 3, 4})
        self.assert_tournament_in_tour('Ewige Tabelle', 'MA4', {1, 2, 3, 4})
        self.assert_tournament_in_tour('Tremonia Series 1000', 'MPO', {1, 2, 3}, expected_evaluate_how_many=7)
        self.assert_tournament_in_tour('Tremonia Series 1000', 'MA4', {1, 2, 3}, expected_evaluate_how_many=7)
        self.assert_tournament_in_tour('Tremonia Series 2000', 'MPO', {4}, expected_evaluate_how_many=7)
        self.assert_tournament_in_tour('Tremonia Series 2000', 'MA4', {4}, expected_evaluate_how_many=7)
        # tournament 5 doesn't have any results and therefore there are no divisions, and it won't be added

    def assert_tournament_in_tour(self, name, division, expected_metrix_ids, expected_evaluate_how_many=10000):
        tour = Tour.objects.get(name=name, division=division)
        tournaments = set(tour.tournaments.all().values_list('metrix_id', flat=True))
        self.assertEqual(tournaments, expected_metrix_ids)
        self.assertEqual(tour.evaluate_how_many, expected_evaluate_how_many)

    def assert_tournament(self, tournaments, id):
        tournament = tournaments.get(metrix_id=id)
        self.assertTrue(tournament.name.startswith(f'Tremonia Series #{id}'))
        self.assertEqual(tournament.url, DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(id))
        self.assertEqual(tournament.begin, date(year=1000 * id, month=1, day=1))
        self.assertEqual(tournament.end, date(year=1000 * id, month=1, day=1))
