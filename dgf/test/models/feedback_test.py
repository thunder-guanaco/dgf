from django.test import TestCase

from .creator import create_friends
from ...models import Feedback


class FeedbackModelTest(TestCase):

    def test_representation(self):
        friend = create_friends(1)
        self.assert_representation(expected='Lorem ipsum', friend=None, title='Lorem ipsum', feedback='')
        self.assert_representation(expected='Friend0 - Lorem ipsum', friend=friend, title='Lorem ipsum', feedback='')

    def assert_representation(self, expected, **fields):
        feedback = Feedback(**fields)
        self.assertEqual(str(feedback), expected)
