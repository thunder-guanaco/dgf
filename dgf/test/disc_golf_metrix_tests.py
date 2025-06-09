from datetime import datetime, timedelta

from django.test import TestCase

from dgf import views
from dgf.disc_golf_metrix import tremonia_series, tremonia_putting_liga
from dgf.models import Tournament
from dgf_cms.settings import DISC_GOLF_METRIX_TOURNAMENT_PAGE

TODAY = datetime.today()
YESTERDAY = TODAY - timedelta(days=1)
TOMORROW = TODAY + timedelta(days=1)
THE_DAY_AFTER_TOMORROW = TODAY + timedelta(days=2)


class DiscGolfMetrixTest(TestCase):

    def setUp(self):
        Tournament.objects.all().delete()

    def test_next_ts(self):
        self.create_ts_tournament(1, YESTERDAY)
        self.create_ts_tournament(2, TODAY)
        self.create_ts_tournament(3, TOMORROW)
        self.create_ts_tournament(4, THE_DAY_AFTER_TOMORROW)

        self.assert_next_ts([2, 3, 4])
        self.assert_next_ts_redirect(2)

    def test_next_ts_only_one(self):
        self.create_ts_tournament(1, YESTERDAY)
        self.create_ts_tournament(2, TODAY)

        self.assert_next_ts([2])
        self.assert_next_ts_redirect(2)

    def test_next_ts_only_one_in_the_future(self):
        self.create_ts_tournament(1, YESTERDAY)
        self.create_ts_tournament(2, TOMORROW)

        self.assert_next_ts([2])
        self.assert_next_ts_redirect(2)

    def test_next_ts_no_tournaments_in_the_future(self):
        self.create_ts_tournament(1, YESTERDAY)

        self.assert_next_ts([])
        self.assert_next_ts_redirect(tremonia_series.ROOT_ID)

    def test_next_ts_no_tournaments_ever(self):
        self.assert_next_ts([])
        self.assert_next_ts_redirect(tremonia_series.ROOT_ID)

    def create_ts_tournament(self, number, date):
        Tournament.objects.create(name=f'Tremonia Series #{number}',
                                  begin=date, end=date, metrix_id=number)

    def assert_next_ts(self, expected_tournaments):
        tournaments = tremonia_series.next_tournaments()
        self.assertEqual([tournament.metrix_id for tournament in tournaments], expected_tournaments)

    def assert_next_ts_redirect(self, expected_metrix_id):
        redirect = views.ts_next_tournament(None)
        self.assertEqual(redirect.url, DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(expected_metrix_id))

    def test_next_tpl(self):
        self.create_tpl_tournament(1, YESTERDAY)
        self.create_tpl_tournament(2, TODAY)
        self.create_tpl_tournament(3, TOMORROW)
        self.create_tpl_tournament(4, THE_DAY_AFTER_TOMORROW)

        self.assert_next_tpl([2, 3, 4])
        self.assert_next_tpl_redirect(2)

    def test_next_tpl_only_one(self):
        self.create_tpl_tournament(1, YESTERDAY)
        self.create_tpl_tournament(2, TODAY)

        self.assert_next_tpl([2])
        self.assert_next_tpl_redirect(2)

    def test_next_tpl_only_one_in_the_future(self):
        self.create_tpl_tournament(1, YESTERDAY)
        self.create_tpl_tournament(2, TOMORROW)

        self.assert_next_tpl([2])
        self.assert_next_tpl_redirect(2)

    def test_next_tpl_no_tournaments_in_the_future(self):
        self.create_tpl_tournament(1, YESTERDAY)

        self.assert_next_tpl([])
        self.assert_next_tpl_redirect(tremonia_putting_liga.ROOT_ID)

    def test_next_tpl_no_tournaments_ever(self):
        self.assert_next_tpl([])
        self.assert_next_tpl_redirect(tremonia_putting_liga.ROOT_ID)

    def create_tpl_tournament(self, number, date):
        Tournament.objects.create(name=f'{number}. Spieltag Tremonia Putting Liga',
                                  begin=date, end=date, metrix_id=number)

    def assert_next_tpl(self, expected_tournaments):
        tournaments = tremonia_putting_liga.next_tournaments()
        self.assertEqual([tournament.metrix_id for tournament in tournaments], expected_tournaments)

    def assert_next_tpl_redirect(self, expected_metrix_id):
        redirect = views.tpl_next_tournament(None)
        self.assertEqual(redirect.url, DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(expected_metrix_id))
