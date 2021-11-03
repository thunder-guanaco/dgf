from django.test import TestCase

from dgf.models import Friend, Tournament, Result


class ResultModelTest(TestCase):

    def test_slug(self):
        self.expect_ordinal('1st', position=1)
        self.expect_ordinal('2nd', position=2)
        self.expect_ordinal('3rd', position=3)
        for i in range(4, 21):
            self.expect_ordinal(f'{i}th', position=i)
        self.expect_ordinal('21st', position=21)
        self.expect_ordinal('22nd', position=22)
        self.expect_ordinal('23rd', position=23)
        for i in range(24, 31):
            self.expect_ordinal(f'{i}th', position=i)

    def expect_ordinal(self, expected_ordinal, position):
        result = Result(friend=Friend(username='test'),
                        tournament=Tournament(name='test'),
                        position=position)
        self.assertEqual(result.ordinal_position, expected_ordinal)
