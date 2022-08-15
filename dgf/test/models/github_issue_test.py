from django.db.utils import IntegrityError
from django.test import TestCase

from .creator import create_friends
from ...models import GitHubIssue


class GitHubIssueModelTest(TestCase):

    def test_representation_no_title(self):
        self.assert_representation(expected=IntegrityError,
                                   title=None, body='dolor sit amet', friend=create_friends(1))

    def test_representation_empty_title(self):
        self.assert_representation(expected='Friend0 -  (Feedback)',
                                   title='', body='dolor sit amet', friend=create_friends(1))

    def test_representation_no_friend(self):
        self.assert_representation(expected='Lorem ipsum (Feedback)',
                                   title='Lorem ipsum', body='', friend=None)

    def test_representation_no_body(self):
        self.assert_representation(expected='Friend0 - Lorem ipsum (Feedback)',
                                   title='Lorem ipsum', body=None, friend=create_friends(1))

    def test_representation_empty_body(self):
        self.assert_representation(expected='Friend0 - Lorem ipsum (Feedback)',
                                   title='Lorem ipsum', body='', friend=create_friends(1))

    def test_representation_full_body(self):
        self.assert_representation(expected='Friend0 - Lorem ipsum (Feedback)',
                                   title='Lorem ipsum', body='dolor sit amet', friend=create_friends(1))

    def test_representation_no_type(self):
        self.assert_representation(expected=IntegrityError,
                                   title='', body='', friend=None, type=None)

    def test_representation_feedback(self):
        self.assert_representation(expected=' (Feedback)',
                                   title='', body='', friend=None, type=GitHubIssue.FEEDBACK)

    def test_representation_live_error(self):
        self.assert_representation(expected=' (Live Error)',
                                   title='', body='', friend=None, type=GitHubIssue.LIVE_ERROR)

    def test_representation_management_command_error(self):
        self.assert_representation(expected=' (Management Command Error)',
                                   title='', body='', friend=None, type=GitHubIssue.MANAGEMENT_COMMAND_ERROR)

    def assert_representation(self, expected, **fields):
        try:
            github_issue = GitHubIssue.objects.create(**fields)
            self.assertEqual(str(github_issue), expected)
        except Exception as e:
            self.assertEqual(type(e), expected)
