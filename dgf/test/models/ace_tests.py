from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from .creator import create_friends, create_courses, create_discs
from ...models import Ace


class AceModelTest(TestCase):

    def test_representation(self):
        self.assert_representation(
            expected=f'Friend0 aced hole 1 at Course0 with a Disc0 ({_("Tournament")}) on 2020-01-01',
            friend=create_friends(1),
            course=create_courses(1),
            disc=create_discs(1),
            hole=1,
            type=Ace.TOURNAMENT,
            date='2020-01-01')
        self.assert_representation(
            expected=f'Friend0 aced hole 1 at Course0 with a Disc0 ({_("Casual Round")})',
            friend=create_friends(1),
            course=create_courses(1),
            disc=create_discs(1),
            hole=1,
            type=Ace.CASUAL_ROUND,
            date=None)

    def assert_representation(self, expected, **fields):
        ace = Ace(**fields)
        self.assertEqual(str(ace), expected)
