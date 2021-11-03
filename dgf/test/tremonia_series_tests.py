import json
from datetime import date

import responses
from django.test import TestCase

from dgf import tremonia_series
from dgf.models import Tournament, Friend
from dgf.tremonia_series import DISC_GOLF_METRIX_COMPETITION_ENDPOINT, TREMONIA_SERIES_ROOT_ID, \
    DISC_GOLF_METRIX_TOURNAMENT_PAGE


class TremoniaSeriesTest(TestCase):

    @responses.activate
    def test_tournaments(self):
        Tournament.objects.all().delete()
        self.add_three_tournaments()

        tremonia_series.update_tournaments()

        tournaments = Tournament.objects.filter(name__startswith='Tremonia Series')
        self.assertEquals(tournaments.count(), 3)
        for id in [1, 2, 3]:
            self.assertTournament(tournaments, id)

    @responses.activate
    def test_tournament_changing_name(self):
        Tournament.objects.all().delete()
        Tournament.objects.create(name='Tremonia Series #28',
                                  begin=date(year=1000, month=1, day=1),
                                  end=date(year=1000, month=1, day=1),
                                  url=DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(12345))
        self.add_one_tournament(12345, 'Tremonia Series #28 (Putter)', '1000-01-01')

        tremonia_series.update_tournaments()

        tournament = Tournament.objects.get(name='Tremonia Series #28 (Putter)')
        self.assertEqual(tournament.name, 'Tremonia Series #28 (Putter)')
        self.assertEqual(tournament.begin, date(year=1000, month=1, day=1))
        self.assertEqual(tournament.end, date(year=1000, month=1, day=1))
        self.assertEqual(tournament.url, DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(12345))

    @responses.activate
    def test_tournament_with_results(self):
        Friend.objects.all().delete()
        Friend.objects.create(username='manolo', first_name='Manolo', metrix_user_id='manolo')
        Friend.objects.create(username='fede', first_name='Federico', metrix_user_id='fede')
        Tournament.objects.all().delete()
        self.add_one_tournament(12345, 'Test', '1000-01-01', players=[('manolo', 1), ('fede', 2)])

        tremonia_series.update_tournaments()

        tournament = Tournament.objects.get(name='Test')
        results = [(result.friend.username, result.position) for result in tournament.results.all()]
        self.assertEqual(results, [('manolo', 1), ('fede', 2)])

    @responses.activate
    def test_tournament_with_results_in_other_format(self):
        Friend.objects.all().delete()
        Friend.objects.create(username='manolo', first_name='Manolo', metrix_user_id='manolo')
        Friend.objects.create(username='fede', first_name='Federico', metrix_user_id='fede')
        Tournament.objects.all().delete()
        self.add_one_tournament(12345, 'Test', '1000-01-01', players=[('manolo', 1), ('fede', 2)], other_format=True)

        tremonia_series.update_tournaments()

        tournament = Tournament.objects.get(name='Test')
        results = [(result.friend.username, result.position) for result in tournament.results.all()]
        self.assertEqual(results, [('manolo', 1), ('fede', 2)])

    @responses.activate
    def test_tournament_with_attendance(self):
        Friend.objects.all().delete()
        Friend.objects.create(username='manolo', first_name='Manolo', metrix_user_id='manolo')
        Friend.objects.create(username='fede', first_name='Federico', metrix_user_id='fede')
        Tournament.objects.all().delete()
        self.add_one_tournament(12345, 'Test', '3000-01-01', players=[('manolo', None), ('fede', None)])

        tremonia_series.update_tournaments()

        tournament = Tournament.objects.get(name='Test')
        attendance = [attendance.friend.username for attendance in tournament.attendance.all()]
        self.assertEqual(attendance, ['manolo', 'fede'])

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

    def add_one_tournament(self, id, name, date_as_str, players=[], other_format=False):
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

    def add_tournament(self, id, name, date_as_str, players=[]):
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

    def add_tournament_with_other_format(self, id, name, date_as_str, players=[]):
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
            position_key: player[1]
        }

    def assertTournament(self, tournaments, id):
        tournament = tournaments.get(name__startswith=f'Tremonia Series #{id}')
        self.assertEqual(tournament.begin, date(year=1000 * id, month=1, day=1))
        self.assertEqual(tournament.end, date(year=1000 * id, month=1, day=1))
        self.assertEqual(tournament.url, DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(id))
