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
    def test_tournament_without_attendance_and_with_empty_attendance(self):
        self.add_tournaments()

        tremonia_series.update_tournaments()

        tournaments = Tournament.objects.filter(name__startswith='Tremonia Series')
        self.assertEquals(tournaments.count(), 3)
        for id in [1, 2, 3]:
            self.assertTournament(tournaments, id)

    def add_tournaments(self):
        responses.add(responses.GET, DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(TREMONIA_SERIES_ROOT_ID),
                      body=json.dumps(
                          {
                              "Competition": {
                                  "Name": "Tremonia Series",
                                  "ID": TREMONIA_SERIES_ROOT_ID,
                                  "Events": [
                                      {
                                          "ID": "1",
                                          "Name": "Tremonia Series #1 (Putter)"  # past tournament
                                      },
                                      {
                                          "ID": "22",
                                          "Name": "[DELETED] Tremonia Series #2"  # canceled
                                      },
                                      {
                                          "ID": "2",
                                          "Name": "Tremonia Series #2 (Midrange)"  # second tournament again
                                      },
                                      {
                                          "ID": "3",
                                          "Name": "Tremonia Series #3"  # future tournament
                                      }
                                  ]
                              }
                          }),
                      status=200)

        responses.add(responses.GET, DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(1),
                      body=json.dumps(
                          {
                              "Competition": {
                                  "ID": 1,
                                  "Name": "Tremonia Series &rarr; Tremonia Series #1 (Putter)",
                                  "Date": "1000-01-01"
                              }
                          }),
                      status=200)

        responses.add(responses.GET, DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(2),
                      body=json.dumps(
                          {
                              "Competition": {
                                  "ID": 2,
                                  "Name": "Tremonia Series &rarr; Tremonia Series #2 (Midrange)",
                                  "Date": "2000-01-01"
                              }
                          }),
                      status=200)

        responses.add(responses.GET, DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(3),
                      body=json.dumps(
                          {
                              "Competition": {
                                  "ID": 3,
                                  "Name": "Tremonia Series &rarr; Tremonia Series #3",
                                  "Date": "3000-01-01"
                              }
                          }),
                      status=200)

    def assertTournament(self, tournaments, id):
        tournament = tournaments.get(name__startswith=f'Tremonia Series #{id}')
        self.assertEquals(tournament.begin, date(year=1000 * id, month=1, day=1))
        self.assertEquals(tournament.end, date(year=1000 * id, month=1, day=1))
        self.assertEquals(tournament.url, DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(id))
