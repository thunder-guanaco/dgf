from django.test import TestCase

from dgf.models import Result, Division
from dgf.test.models.creator import create_friends, create_tournaments, create_divisions


class ResultModelTest(TestCase):

    def test_representation(self):
        create_divisions()
        result = Result(friend=create_friends(1),
                        tournament=create_tournaments(1),
                        position=1,
                        division=Division.objects.get(id='MPO'))
        self.assertEqual(str(result), 'Friend0 was 1st at Tournament0 (01. Jan. 2020) in the "MPO - Pro Open" division')

    def test_representation_with_points(self):
        create_divisions()
        result = Result(friend=create_friends(1),
                        tournament=create_tournaments(1),
                        position=1,
                        points=200,
                        division=Division.objects.get(id='MPO'))
        self.assertEqual(str(result), 'Friend0 was 1st (200 points) '
                                      'at Tournament0 (01. Jan. 2020) in the "MPO - Pro Open" division')

    def test_ordinal(self):
        self.assert_ordinal('1st', position=1)
        self.assert_ordinal('2nd', position=2)
        self.assert_ordinal('3rd', position=3)
        for i in range(4, 21):
            self.assert_ordinal(f'{i}th', position=i)
        self.assert_ordinal('21st', position=21)
        self.assert_ordinal('22nd', position=22)
        self.assert_ordinal('23rd', position=23)
        for i in range(24, 31):
            self.assert_ordinal(f'{i}th', position=i)

    def assert_ordinal(self, expected, position):
        result = Result(friend=create_friends(1),
                        tournament=create_tournaments(1),
                        position=position)
        self.assertEqual(result.ordinal_position, expected)
