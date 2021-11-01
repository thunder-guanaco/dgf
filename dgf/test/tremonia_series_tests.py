import json
from datetime import date

import responses
from django.test import TestCase

from dgf import tremonia_series
from dgf.models import Tournament
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

        tournaments = Tournament.objects.filter(name__startswith='Tremonia Series')
        self.assertEquals(tournaments.count(), 1)
        tournament = tournaments[0]
        self.assertEquals(tournament.name, 'Tremonia Series #28 (Putter)')
        self.assertEquals(tournament.begin, date(year=1000, month=1, day=1))
        self.assertEquals(tournament.end, date(year=1000, month=1, day=1))
        self.assertEquals(tournament.url, DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(12345))

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

    def add_one_tournament(self, id, name, date_as_str):
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

        self.add_tournament(id, name, date_as_str)

    def add_tournament(self, id, name, date_as_str):
        responses.add(responses.GET, DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(id),
                      body=json.dumps(
                          {
                              'Competition': {
                                  'ID': id,
                                  'Name': f'Tremonia Series &rarr; {name}',
                                  'Date': date_as_str
                              }
                          }),
                      status=200)

    def assertTournament(self, tournaments, id):
        tournament = tournaments.get(name__startswith=f'Tremonia Series #{id}')
        self.assertEquals(tournament.begin, date(year=1000 * id, month=1, day=1))
        self.assertEquals(tournament.end, date(year=1000 * id, month=1, day=1))
        self.assertEquals(tournament.url, DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(id))
