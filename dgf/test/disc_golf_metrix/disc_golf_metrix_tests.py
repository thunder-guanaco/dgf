from datetime import datetime, timedelta

from django.test import TestCase

from dgf import views
from dgf.disc_golf_metrix import disc_golf_metrix
from dgf.disc_golf_metrix.tremonia_series import TREMONIA_SERIES_ROOT_ID
from dgf.models import Tournament
from dgf_cms.settings import DISC_GOLF_METRIX_TOURNAMENT_PAGE

TODAY = datetime.today()
YESTERDAY = TODAY - timedelta(days=1)
TOMORROW = TODAY + timedelta(days=1)
THE_DAY_AFTER_TOMORROW = TODAY + timedelta(days=2)


class DiscGolfMetrixTest(TestCase):

    def setUp(self):
        Tournament.objects.all().delete()

    def test_next_tournaments(self):
        self.create_tournament('Tremonia Series #1', YESTERDAY)
        self.create_tournament('Tremonia Series #2', TODAY)
        self.create_tournament('Tremonia Series #3', TOMORROW)
        self.create_tournament('Tremonia Series #4', THE_DAY_AFTER_TOMORROW)

        self.assert_next_tournaments(['Tremonia Series #2', 'Tremonia Series #3', 'Tremonia Series #4'])
        self.assert_next_tournament_redirect(2)

    def test_next_tournaments_only_one(self):
        self.create_tournament('Tremonia Series #1', YESTERDAY)
        self.create_tournament('Tremonia Series #2', TODAY)

        self.assert_next_tournaments(['Tremonia Series #2'])
        self.assert_next_tournament_redirect(2)

    def test_next_tournaments_no_tournaments(self):
        self.create_tournament('Tremonia Series #1', YESTERDAY)

        self.assert_next_tournaments([])
        self.assert_next_tournament_redirect(TREMONIA_SERIES_ROOT_ID)

    def test_next_tournaments_no_tournaments_ever(self):
        self.assert_next_tournaments([])
        self.assert_next_tournament_redirect(TREMONIA_SERIES_ROOT_ID)

    def create_tournament(self, name, date):
        Tournament.objects.create(name=name, begin=date, end=date, metrix_id=name.split('#')[-1])

    def assert_next_tournaments(self, expected_tournaments):
        tournaments = disc_golf_metrix.next_tournaments('Tremonia Series')
        self.assertEqual([tournament.name for tournament in tournaments], expected_tournaments)

    def assert_next_tournament_redirect(self, expected_metrix_id):
        redirect = views.ts_next_tournament('Tremonia Series')
        self.assertEqual(redirect.url, DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(expected_metrix_id))
