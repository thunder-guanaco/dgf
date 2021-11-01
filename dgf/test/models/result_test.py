from django.test import TestCase

from dgf.models import Friend, Tournament, Result


class ResultModelTest(TestCase):

    def test_slug(self):
        self.expect_ordinal('1st', position=1)
        self.expect_ordinal('2nd', position=2)
        self.expect_ordinal('3rd', position=3)
        self.expect_ordinal('4th', position=4)
        self.expect_ordinal('5th', position=5)
        self.expect_ordinal('6th', position=6)
        self.expect_ordinal('7th', position=7)
        self.expect_ordinal('8th', position=8)
        self.expect_ordinal('9th', position=9)
        self.expect_ordinal('10th', position=10)
        self.expect_ordinal('11th', position=11)
        self.expect_ordinal('12th', position=12)
        self.expect_ordinal('13th', position=13)
        self.expect_ordinal('14th', position=14)
        self.expect_ordinal('15th', position=15)
        self.expect_ordinal('16th', position=16)
        self.expect_ordinal('17th', position=17)
        self.expect_ordinal('18th', position=18)
        self.expect_ordinal('19th', position=19)
        self.expect_ordinal('20th', position=20)
        self.expect_ordinal('21st', position=21)
        self.expect_ordinal('22nd', position=22)
        self.expect_ordinal('23rd', position=23)
        self.expect_ordinal('24th', position=24)
        self.expect_ordinal('25th', position=25)
        self.expect_ordinal('26th', position=26)
        self.expect_ordinal('27th', position=27)
        self.expect_ordinal('28th', position=28)
        self.expect_ordinal('29th', position=29)
        self.expect_ordinal('30th', position=30)

    def expect_ordinal(self, expected_ordinal, position):
        result = Result(friend=Friend(username='test'),
                        tournament=Tournament(name='test'),
                        position=position)
        self.assertEqual(result.ordinal_position, expected_ordinal)
