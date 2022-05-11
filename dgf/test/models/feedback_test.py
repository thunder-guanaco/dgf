from django.db.utils import IntegrityError
from django.test import TestCase

from .creator import create_friends
from ...models import Feedback


class FeedbackModelTest(TestCase):

    def test_representation(self):
        friend = create_friends(1)
        self.assert_representation(expected='Lorem ipsum',
                                   friend=None, title='Lorem ipsum', feedback='')

        self.assert_representation(expected='Friend0 - Lorem ipsum',
                                   friend=friend, title='Lorem ipsum', feedback=None)

        self.assert_representation(expected='Friend0 - Lorem ipsum',
                                   friend=friend, title='Lorem ipsum', feedback='')

        self.assert_representation(expected='Friend0 - Lorem ipsum',
                                   friend=friend, title='Lorem ipsum', feedback='dolor sit amet')

        self.assert_representation(expected=IntegrityError,
                                   friend=friend, title=None, feedback='dolor sit amet')

    def assert_representation(self, expected, **fields):
        try:
            feedback = Feedback.objects.create(**fields)
            self.assertEqual(str(feedback), expected)
        except Exception as e:
            self.assertEqual(type(e), expected)
