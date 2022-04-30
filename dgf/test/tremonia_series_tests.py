import json
from datetime import date

import responses
from django.test import TestCase

from dgf import tremonia_series
from dgf.models import Tournament, Friend, Attendance, Result, Tour, Division
from dgf.test.models.creator import create_divisions
from dgf.tremonia_series import DISC_GOLF_METRIX_COMPETITION_ENDPOINT, TREMONIA_SERIES_ROOT_ID
from dgf_cms.settings import DISC_GOLF_METRIX_TOURNAMENT_PAGE


class TremoniaSeriesTest(TestCase):

    def setUp(self):
        Tournament.objects.all().delete()
        Tour.objects.all().delete()
        Friend.objects.all().delete()
        Division.objects.all().delete()
        create_divisions()

    @responses.activate
    def test_tournaments(self):
        self.add_three_tournaments()

        tremonia_series.update_tournaments()

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
        self.add_one_tournament(12345, 'Tremonia Series #28 (Putter)', '1000-01-01')

        tremonia_series.update_tournaments()

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
        self.add_one_tournament(12345, 'Tremonia Series #28 (Putter)', '1000-01-01')

        tremonia_series.update_tournaments()

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
        self.add_one_tournament(12345, 'Tremonia Series #28 (Putter)', '1000-01-01')

        tremonia_series.update_tournaments()

        tournament = Tournament.objects.get(metrix_id=12345)
        self.assertEqual(tournament.name, 'Tremonia Series #28 (Putter)')
        self.assertEqual(tournament.url, DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(12345))
        self.assertEqual(tournament.begin, date(year=1000, month=1, day=1))
        self.assertEqual(tournament.end, date(year=1000, month=1, day=1))

    @responses.activate
    def test_tournament_with_results(self):
        Friend.objects.create(username='manolo', first_name='Manolo', metrix_user_id='manolo')
        Friend.objects.create(username='fede', first_name='Federico', metrix_user_id='fede')
        self.add_one_tournament(12345, 'Test', '1000-01-01', players=[('manolo', 1, ''), ('fede', 2, '')])

        tremonia_series.update_tournaments()

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
        self.add_one_tournament(12345, 'Test', '1000-01-01', players=[('manolo', 1, 'Open'),
                                                                      ('david', 2, 'Open'),
                                                                      ('chris', 3, 'Open'),
                                                                      ('jan', 1, 'Amateur'),
                                                                      ('anna', 2, 'Amateur'),
                                                                      ('marcel', 3, 'Amateur')])

        tremonia_series.update_tournaments()

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
        self.add_one_tournament(12345, 'Test', '1000-01-01', players=[('manolo', 1, ''), ('fede', 2, '')])

        tremonia_series.update_tournaments()

        tournament = Tournament.objects.get(metrix_id=12345)
        self.assertEqual(tournament.results.all().count(), 2)  # no results were added
        results = [(result.friend.username, result.position, result.division.id) for result in
                   tournament.results.all().order_by('position')]
        self.assertEqual(results, [('fede', 1, 'MPO'), ('manolo', 2, 'MPO')])

    @responses.activate
    def test_tournament_with_results_and_points(self):
        Friend.objects.create(username='manolo', first_name='Manolo', metrix_user_id='manolo')
        Friend.objects.create(username='fede', first_name='Federico', metrix_user_id='fede')
        self.add_one_tournament(12345, 'Test', '1000-01-01', players=[('manolo', 1, ''), ('fede', 2, '')])

        tremonia_series.update_tournaments()

        tournament = Tournament.objects.get(metrix_id=12345)
        results = [(result.friend.username, result.position, result.division.id, result.points) for result in
                   tournament.results.all().order_by('position')]
        self.assertEqual(results, [('manolo', 1, 'MPO', 20), ('fede', 2, 'MPO', 17)])

    @responses.activate
    def test_tournament_with_results_in_other_format(self):
        Friend.objects.create(username='manolo', first_name='Manolo', metrix_user_id='manolo')
        Friend.objects.create(username='fede', first_name='Federico', metrix_user_id='fede')
        self.add_one_tournament(12345, 'Test', '1000-01-01',
                                players=[('manolo', 1, ''), ('fede', 2, '')],
                                other_format=True)

        tremonia_series.update_tournaments()

        tournament = Tournament.objects.get(metrix_id=12345)
        results = [(result.friend.username, result.position, result.division.id) for result in
                   tournament.results.all().order_by('position')]
        self.assertEqual(results, [('manolo', 1, 'MPO'), ('fede', 2, 'MPO')])

    @responses.activate
    def test_tournament_with_attendance(self):
        Friend.objects.create(username='manolo', first_name='Manolo', metrix_user_id='manolo')
        Friend.objects.create(username='fede', first_name='Federico', metrix_user_id='fede')
        self.add_one_tournament(12345, 'Test', '3000-01-01', players=[('manolo', None, ''), ('fede', None, '')])

        tremonia_series.update_tournaments()

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
        self.add_one_tournament(12345, 'Test', '3000-01-01', players=[('manolo', None, ''), ('fede', None, '')])

        tremonia_series.update_tournaments()

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
        self.add_one_tournament(12345, 'Test', '3000-01-01', players=[('manolo', None, ''), ('fede', None, '')])

        tremonia_series.update_tournaments()

        tournament = Tournament.objects.get(metrix_id=12345)
        attendance = set(tournament.attendance.all().values_list('friend__username', flat=True))
        self.assertEqual(attendance, {'manolo', 'fede'})

    @responses.activate
    def test_add_automatic_tours(self):
        Tournament.objects.create(metrix_id=1,
                                  name='Tremonia Series #1',
                                  begin=date(year=1000, month=1, day=1),
                                  end=date(year=1000, month=1, day=1))
        Tournament.objects.create(metrix_id=2,
                                  name='Tremonia Series #2',
                                  begin=date(year=1000, month=2, day=2),
                                  end=date(year=1000, month=2, day=2))
        self.add_five_tournaments_for_tours()

        tremonia_series.update_tournaments()

        self.assert_tournament_in_tour('Ewige Tabelle', {1, 2, 3, 4, 5})
        self.assert_tournament_in_tour('Tremonia Series 1000', {1, 2, 3})  # 1 and 2 already exists but had no tours
        self.assert_tournament_in_tour('Tremonia Series 2000', {4, 5})

    def assert_tournament_in_tour(self, tour_name, expected_metrix_ids):
        tour = Tour.objects.get(name=tour_name)
        tournaments = set(tour.tournaments.all().values_list('metrix_id', flat=True))
        self.assertEqual(tournaments, expected_metrix_ids)

    def add_three_tournaments(self):
        responses.add(responses.GET, DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(TREMONIA_SERIES_ROOT_ID),
                      body=json.dumps(
                          {
                              'Competition': {
                                  'Name': 'Tremonia Series',
                                  'ID': TREMONIA_SERIES_ROOT_ID,
                                  'Events': [
                                      {
                                          'ID': '1',
                                          'Name': 'Tremonia Series #1 (Putter)'  # past tournament
                                      },
                                      {
                                          'ID': '22',
                                          'Name': '[DELETED] Tremonia Series #2'  # canceled
                                      },
                                      {
                                          'ID': '2',
                                          'Name': 'Tremonia Series #2 (Midrange)'  # second tournament again
                                      },
                                      {
                                          'ID': '3',
                                          'Name': 'Tremonia Series #3'  # future tournament
                                      }
                                  ]
                              }
                          }),
                      status=200)

        self.add_tournament(1, 'Tremonia Series #1 (Putter)', '1000-01-01')
        self.add_tournament(2, 'Tremonia Series #2 (Midrange)', '2000-01-01')
        self.add_tournament(3, 'Tremonia Series #3', '3000-01-01')

    def add_five_tournaments_for_tours(self):
        responses.add(responses.GET, DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(TREMONIA_SERIES_ROOT_ID),
                      body=json.dumps(
                          {
                              'Competition': {
                                  'Name': 'Tremonia Series',
                                  'ID': TREMONIA_SERIES_ROOT_ID,
                                  'Events': [
                                      {
                                          'ID': '1',
                                          'Name': 'Tremonia Series #1'
                                      },
                                      {
                                          'ID': '2',
                                          'Name': 'Tremonia Series #2'
                                      },
                                      {
                                          'ID': '3',
                                          'Name': 'Tremonia Series #3'
                                      },
                                      {
                                          'ID': '4',
                                          'Name': 'Tremonia Series #4'
                                      },
                                      {
                                          'ID': '5',
                                          'Name': 'Tremonia Series #5'
                                      }
                                  ]
                              }
                          }),
                      status=200)

        self.add_tournament(1, 'Tremonia Series #1', '1000-01-01')
        self.add_tournament(2, 'Tremonia Series #2', '1000-02-02')
        self.add_tournament(3, 'Tremonia Series #3', '1000-03-03')
        self.add_tournament(4, 'Tremonia Series #4', '2000-01-01')
        self.add_tournament(5, 'Tremonia Series #5', '2000-02-02')

    def add_one_tournament(self, id, name, date_as_str, players=None, other_format=False):
        responses.add(responses.GET, DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(TREMONIA_SERIES_ROOT_ID),
                      body=json.dumps(
                          {
                              'Competition': {
                                  'Name': 'Tremonia Series',
                                  'ID': TREMONIA_SERIES_ROOT_ID,
                                  'Events': [
                                      {
                                          'ID': f'{id}',
                                          'Name': name
                                      },
                                  ]
                              }
                          }),
                      status=200)

        if other_format:
            self.add_tournament_with_other_format(id, name, date_as_str, players=players)
        else:
            self.add_tournament(id, name, date_as_str, players=players)

    def add_tournament(self, id, name, date_as_str, players=None):
        if not players:
            players = []
        responses.add(responses.GET, DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(id),
                      body=json.dumps(
                          {
                              'Competition': {
                                  'ID': id,
                                  'Name': f'Tremonia Series &rarr; {name}',
                                  'Date': date_as_str,
                                  'TourResults': [self.result(player, 'Place') for player in players]
                              }
                          }),
                      status=200)

    def add_tournament_with_other_format(self, id, name, date_as_str, players=None):
        if not players:
            players = []
        responses.add(responses.GET, DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(id),
                      body=json.dumps(
                          {
                              'Competition': {
                                  'ID': id,
                                  'Name': f'Tremonia Series &rarr; {name}',
                                  'Date': date_as_str,
                                  'SubCompetitions':
                                      [
                                          {
                                              'Results': [self.result(player, 'OrderNumber') for player in
                                                          players]
                                          }
                                      ]
                              }
                          }),
                      status=200)

    def result(self, player, position_key):
        return {
            'UserID': player[0],
            'Name': player[0],
            position_key: player[1],
            'ClassName': player[2],
        }

    def assert_tournament(self, tournaments, id):
        tournament = tournaments.get(metrix_id=id)
        self.assertTrue(tournament.name.startswith(f'Tremonia Series #{id}'))
        self.assertEqual(tournament.url, DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(id))
        self.assertEqual(tournament.begin, date(year=1000 * id, month=1, day=1))
        self.assertEqual(tournament.end, date(year=1000 * id, month=1, day=1))
