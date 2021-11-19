from django.test import TestCase

from dgf.templatetags.dgf import metrix_url, ts_number
from dgf.test.models.creator import create_tournaments


class TemplatetagsTournamentsTest(TestCase):

    def test_metrix_url(self):
        tournament = create_tournaments(1)
        tournament.metrix_id = 123
        tournament.save()
        self.assertEqual(metrix_url(tournament), 'https://discgolfmetrix.com/123')

    def test_metrix_url_without_id(self):
        tournament = create_tournaments(1)
        tournament.metrix_id = None
        tournament.save()
        self.assertEqual(metrix_url(tournament), '')

    def test_ts_number(self):
        tournament = create_tournaments(1)
        tournament.name = 'Tremonia Series #1'
        tournament.save()
        self.assertEqual(ts_number(tournament), 'TS#1')

    def test_metrix_url_with_text_after_number(self):
        tournament = create_tournaments(1)
        tournament.name = 'Tremonia Series #1 (Putter)'
        tournament.save()
        self.assertEqual(ts_number(tournament), 'TS#1')

    def test_metrix_url_with_no_ts_tournament(self):
        tournament = create_tournaments(1)
        tournament.name = 'Tremonia Open 2020'
        tournament.save()
        self.assertEqual(ts_number(tournament), '')
