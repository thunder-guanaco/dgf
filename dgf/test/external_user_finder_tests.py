from django.test import TestCase

from dgf import external_user_finder
from dgf.models import Friend


class ExternalUserFinderTest(TestCase):

    def test_find_existing_friend_by_metrix_user_id(self):
        Friend.all_objects.all().delete()
        expected = Friend.objects.create(username='manolo',
                                         metrix_user_id='123')

        friend = external_user_finder.find_friend(metrix_user_id='123', name='Manuel García García')

        self.assertEqual(friend.username, expected.username)

    def test_find_existing_friend_by_username(self):
        Friend.all_objects.all().delete()
        expected = Friend.objects.create(username='manuel-garcia-garcia')

        friend = external_user_finder.find_friend(metrix_user_id='123', name='Manuel García García')

        self.assertEqual(friend.username, expected.username)
        self.assertEqual(friend.metrix_user_id, '123')

    def test_find_existing_friend_by_username_without_metrix_user_id(self):
        Friend.all_objects.all().delete()
        expected = Friend.objects.create(username='manuel-garcia-garcia')

        friend = external_user_finder.find_friend(metrix_user_id=None, name='Manuel García García')

        self.assertEqual(friend.username, expected.username)
        self.assertEqual(friend.metrix_user_id, None)

    def test_find_existing_friend_by_username_with_weird_stuff(self):
        Friend.all_objects.all().delete()
        expected = Friend.objects.create(username='manuel-garcia-garcia')

        friend = external_user_finder.find_friend(metrix_user_id='123', name='Manuel, García García')

        self.assertEqual(friend.username, expected.username)

    def test_find_existing_friend_by_name(self):
        Friend.all_objects.all().delete()
        expected = Friend.objects.create(username='manolo',
                                         first_name='Manuel',
                                         last_name='García García')

        friend = external_user_finder.find_friend(metrix_user_id='123', name='Manuel García García')

        self.assertEqual(friend.username, expected.username)
        self.assertEqual(friend.metrix_user_id, '123')

    def test_find_existing_friend_by_name_without_metrix_user_id(self):
        Friend.all_objects.all().delete()
        expected = Friend.objects.create(username='manolo',
                                         first_name='Manuel',
                                         last_name='García García')

        friend = external_user_finder.find_friend(metrix_user_id=None, name='Manuel García García')

        self.assertEqual(friend.username, expected.username)
        self.assertEqual(friend.metrix_user_id, None)

    def test_find_non_existing_friend(self):
        Friend.all_objects.all().delete()

        friend = external_user_finder.find_friend(metrix_user_id='123', name='Manuel García García')

        self.assertEqual(friend.username, 'manuel-garcia-garcia')
        self.assertEqual(friend.slug, 'manuel-garcia-garcia')
        self.assertEqual(friend.first_name, 'Manuel')
        self.assertEqual(friend.last_name, 'García García')
        self.assertEqual(friend.metrix_user_id, '123')
        self.assertEqual(friend.is_active, False)

    def test_find_non_existing_friend_without_metrix_user_id(self):
        Friend.all_objects.all().delete()

        friend = external_user_finder.find_friend(metrix_user_id=None, name='Manuel García García')

        self.assertEqual(friend.username, 'manuel-garcia-garcia')
        self.assertEqual(friend.slug, 'manuel-garcia-garcia')
        self.assertEqual(friend.first_name, 'Manuel')
        self.assertEqual(friend.last_name, 'García García')
        self.assertEqual(friend.metrix_user_id, None)
        self.assertEqual(friend.is_active, False)

    def test_find_non_existing_friend_with_similar_existing_friends(self):
        Friend.all_objects.all().delete()
        Friend.objects.create(username='manolo',
                              slug='manolo',
                              first_name='Manuel',
                              last_name='García García')
        Friend.objects.create(username='manolo2',
                              slug='manol2',
                              first_name='Manuel',
                              last_name='García García')

        friend = external_user_finder.find_friend(metrix_user_id='123', name='Manuel García García')

        self.assertEqual(friend.username, 'manuel-garcia-garcia')
        self.assertEqual(friend.slug, 'manuel-garcia-garcia')
        self.assertEqual(friend.first_name, 'Manuel')
        self.assertEqual(friend.last_name, 'García García')
        self.assertEqual(friend.metrix_user_id, '123')
        self.assertEqual(friend.is_active, False)

    def test_find_non_existing_friend_with_similar_existing_friends_without_metrix_user_id(self):
        Friend.all_objects.all().delete()
        Friend.objects.create(username='manolo',
                              slug='manolo',
                              first_name='Manuel',
                              last_name='García García')
        Friend.objects.create(username='manolo2',
                              slug='manol2',
                              first_name='Manuel',
                              last_name='García García')

        friend = external_user_finder.find_friend(metrix_user_id=None, name='Manuel García García')

        self.assertEqual(friend.username, 'manuel-garcia-garcia')
        self.assertEqual(friend.slug, 'manuel-garcia-garcia')
        self.assertEqual(friend.first_name, 'Manuel')
        self.assertEqual(friend.last_name, 'García García')
        self.assertEqual(friend.metrix_user_id, None)
        self.assertEqual(friend.is_active, False)
