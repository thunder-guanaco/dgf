from datetime import date
from unittest import TestCase

import responses

from dgf.models import Friend, Tournament
from dgf.pdga import PdgaApi
from dgf.test.pdga.tournaments.responses import add_login

APRIL_2 = date(year=2021, month=4, day=2)
JULY_24 = date(year=2021, month=7, day=24)
JULY_25 = date(year=2021, month=7, day=25)
JULY_26 = date(year=2021, month=7, day=26)


class PdgaTournamentTest(TestCase):

    @responses.activate
    def setUp(self):
        Friend.objects.all().delete()
        Tournament.objects.all().delete()
        responses.reset()
        add_login()
        self.pdga_api = PdgaApi()

    def assert_tournament_amount(self, amount):
        self.assertEqual(Tournament.objects.all().count(), amount, f'there should be {amount} Tournament objects')

    def assert_tournament_exists(self, pdga_id, name, begin, end, url):
        tournament = Tournament.objects.get(pdga_id=pdga_id)
        self.assertEqual(tournament.name, name, 'name does not match')
        self.assertEqual(tournament.begin, begin, 'begin does not match')
        self.assertEqual(tournament.end, end, 'end does not match')
        self.assertEqual(tournament.url, url, 'url does not match')
