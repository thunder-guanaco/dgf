from django.test import TestCase

from dgf.templatetags.dgf import metrix_url, short_name, short_name_mobile
from dgf.test.models.creator import create_tournaments


class DiscGolfMetrixTemplatetagsTest(TestCase):

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

    def test_short_name(self):
        self.assert_that(with_name='Tremonia Series #1', expect_short_name='TS#1')
        self.assert_that(with_name='Tremonia Series #1 (Putter)', expect_short_name='TS#1')
        self.assert_that(with_name='1. Spieltag Tremonia Putting Liga', expect_short_name='1. Spieltag')
        self.assert_that(with_name='Tremonia Open 2020', expect_short_name='')
        self.assert_that(with_name='Tremonia Series #1', expect_short_name='#1', mobile=True)
        self.assert_that(with_name='Tremonia Series #1 (Putter)', expect_short_name='#1', mobile=True)
        self.assert_that(with_name='1. Spieltag Tremonia Putting Liga', expect_short_name='1', mobile=True)
        self.assert_that(with_name='Tremonia Open 2020', expect_short_name='', mobile=True)

    def assert_that(self, with_name, expect_short_name, mobile=False):
        tournament = create_tournaments(1)
        tournament.name = with_name
        tournament.save()
        short_name_result = short_name_mobile(tournament) if mobile else short_name(tournament)
        self.assertEqual(short_name_result, expect_short_name)
