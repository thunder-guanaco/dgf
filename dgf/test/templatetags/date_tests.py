from datetime import datetime
from unittest.mock import patch

from django.test import TestCase

from dgf.templatetags import dgf


class DateTemplatetagsTest(TestCase):

    @patch('django.utils.timezone.now')
    def test_days_since(self, mock_timezone):
        # 10 days no matter what hour of the day
        self.assertWith(mock_timezone,
                        from_change=datetime(2023, 1, 1, 10, 0),
                        until_today=datetime(2023, 1, 11, 11, 0),
                        expect=10)
        self.assertWith(mock_timezone,
                        from_change=datetime(2023, 1, 1, 10, 0),
                        until_today=datetime(2023, 1, 11, 10, 0),
                        expect=10)
        self.assertWith(mock_timezone,
                        from_change=datetime(2023, 1, 1, 10, 0),
                        until_today=datetime(2023, 1, 11, 9, 0),
                        expect=10)

        # 1 day no matter what hour of the day
        self.assertWith(mock_timezone,
                        from_change=datetime(2023, 1, 1, 10, 0),
                        until_today=datetime(2023, 1, 2, 11, 0),
                        expect=1)
        self.assertWith(mock_timezone,
                        from_change=datetime(2023, 1, 1, 10, 0),
                        until_today=datetime(2023, 1, 2, 10, 0),
                        expect=1)
        self.assertWith(mock_timezone,
                        from_change=datetime(2023, 1, 1, 10, 0),
                        until_today=datetime(2023, 1, 2, 9, 0),
                        expect=1)

        # 0 days no matter what hour of the day
        self.assertWith(mock_timezone,
                        from_change=datetime(2023, 1, 1, 10, 0),
                        until_today=datetime(2023, 1, 1, 11, 0),
                        expect=0)
        self.assertWith(mock_timezone,
                        from_change=datetime(2023, 1, 1, 10, 0),
                        until_today=datetime(2023, 1, 1, 10, 0),
                        expect=0)

    def assertWith(self, mock_timezone, from_change=None, until_today=None, expect=0):
        mock_timezone.return_value = until_today
        self.assertEqual(dgf.days_since(from_change), expect)
