from django.test import TestCase

from dgf import external_user_finder
from dgf.models import Friend


class ExternalUserFinderTest(TestCase):

    def test_find_existing_friend_by_metrix_user_id(self):
        Friend.all_objects.all().delete()
        existing_friend = Friend.objects.create(username='manolo',
                                                metrix_user_id='123',
                                                first_name='Manuel',
                                                last_name='García García',
                                                is_active=True)

        friend = external_user_finder.find_friend(metrix_user_id='123', name='Manolo García')

        self.assertEqual(friend.username, existing_friend.username)
        self.assertEqual(friend.metrix_user_id, existing_friend.metrix_user_id)
        self.assertEqual(friend.first_name, existing_friend.first_name)
        self.assertEqual(friend.last_name, existing_friend.last_name)
        self.assertEqual(friend.slug, existing_friend.slug)
        self.assertEqual(friend.is_active, existing_friend.is_active)

    def test_find_existing_inactive_friend_by_metrix_user_id(self):
        Friend.all_objects.all().delete()
        existing_friend = Friend.objects.create(username='manolo',
                                                metrix_user_id='123',
                                                first_name='Manuel',
                                                last_name='García García',
                                                is_active=False)

        friend = external_user_finder.find_friend(metrix_user_id='123', name='Manolo García')

        self.assertEqual(friend.username, existing_friend.username)
        self.assertEqual(friend.slug, existing_friend.slug)
        self.assertEqual(friend.metrix_user_id, existing_friend.metrix_user_id)
        self.assertEqual(friend.first_name, 'Manolo')
        self.assertEqual(friend.last_name, 'García')
        self.assertEqual(friend.is_active, False)

    def test_find_existing_inactive_friend_by_metrix_user_id_without_name(self):
        Friend.all_objects.all().delete()
        existing_friend = Friend.objects.create(username='manolo',
                                                metrix_user_id='123',
                                                first_name='Manuel',
                                                last_name='García García',
                                                is_active=False)

        friend = external_user_finder.find_friend(metrix_user_id='123', name='')

        self.assertEqual(friend.username, existing_friend.username)
        self.assertEqual(friend.metrix_user_id, existing_friend.metrix_user_id)
        self.assertEqual(friend.first_name, existing_friend.first_name)
        self.assertEqual(friend.last_name, existing_friend.last_name)
        self.assertEqual(friend.slug, existing_friend.slug)
        self.assertEqual(friend.is_active, existing_friend.is_active)

    def test_find_existing_friend_by_username(self):
        Friend.all_objects.all().delete()
        existing_friend = Friend.objects.create(username='manuel-garcia-garcia',
                                                first_name='Manolo',
                                                last_name='García',
                                                is_active=True)

        friend = external_user_finder.find_friend(metrix_user_id='123', name='Manuel García García')

        self.assertEqual(friend.username, existing_friend.username)
        self.assertEqual(friend.metrix_user_id, None)
        self.assertEqual(friend.first_name, existing_friend.first_name)
        self.assertEqual(friend.last_name, existing_friend.last_name)
        self.assertEqual(friend.slug, existing_friend.slug)
        self.assertEqual(friend.is_active, existing_friend.is_active)

    def test_find_existing_inactive_friend_by_username(self):
        Friend.all_objects.all().delete()
        existing_friend = Friend.objects.create(username='manuel-garcia-garcia',
                                                first_name='Manolo',
                                                last_name='García',
                                                is_active=False)

        friend = external_user_finder.find_friend(metrix_user_id='123', name='Manuel García García')

        self.assertEqual(friend.username, existing_friend.username)
        self.assertEqual(friend.slug, existing_friend.slug)
        self.assertEqual(friend.metrix_user_id, '123')
        self.assertEqual(friend.first_name, 'Manuel')
        self.assertEqual(friend.last_name, 'García García')
        self.assertEqual(friend.is_active, existing_friend.is_active)

    def test_find_existing_friend_by_username_without_metrix_user_id(self):
        Friend.all_objects.all().delete()
        existing_friend = Friend.objects.create(metrix_user_id='123',
                                                username='manuel-garcia-garcia',
                                                first_name='Manolo',
                                                last_name='García',
                                                is_active=False)

        friend = external_user_finder.find_friend(metrix_user_id=None, name='Manuel García García')

        self.assertEqual(friend.username, existing_friend.username)
        self.assertEqual(friend.slug, existing_friend.slug)
        self.assertEqual(friend.metrix_user_id, existing_friend.metrix_user_id)
        self.assertEqual(friend.first_name, 'Manuel')
        self.assertEqual(friend.last_name, 'García García')
        self.assertEqual(friend.is_active, existing_friend.is_active)

    def test_find_existing_friend_by_username_with_weird_stuff(self):
        Friend.all_objects.all().delete()
        existing_friend = Friend.objects.create(username='manuel-garcia-garcia')

        friend = external_user_finder.find_friend(metrix_user_id='123', name='Manuel, García García')

        self.assertEqual(friend.username, existing_friend.username)

    def test_find_existing_friend_by_name(self):
        Friend.all_objects.all().delete()
        existing_friend = Friend.objects.create(metrix_user_id='123',
                                                username='manolo',
                                                first_name='Manuel',
                                                last_name='García García',
                                                is_active=True)

        friend = external_user_finder.find_friend(metrix_user_id='456', name='Manuel García García')

        self.assertEqual(friend.username, existing_friend.username)
        self.assertEqual(friend.metrix_user_id, existing_friend.metrix_user_id)
        self.assertEqual(friend.first_name, existing_friend.first_name)
        self.assertEqual(friend.last_name, existing_friend.last_name)
        self.assertEqual(friend.slug, existing_friend.slug)
        self.assertEqual(friend.is_active, existing_friend.is_active)

    def test_find_existing_inactive_friend_by_name(self):
        Friend.all_objects.all().delete()
        existing_friend = Friend.objects.create(metrix_user_id='123',
                                                username='manolo',
                                                first_name='Manuel',
                                                last_name='García García',
                                                is_active=False)

        friend = external_user_finder.find_friend(metrix_user_id='456', name='Manuel García García')

        self.assertEqual(friend.username, existing_friend.username)
        self.assertEqual(friend.slug, existing_friend.slug)
        self.assertEqual(friend.metrix_user_id, '456')
        self.assertEqual(friend.first_name, 'Manuel')
        self.assertEqual(friend.last_name, 'García García')
        self.assertEqual(friend.is_active, False)

    def test_find_existing_friend_by_name_without_metrix_user_id(self):
        Friend.all_objects.all().delete()
        existing_friend = Friend.objects.create(metrix_user_id='123',
                                                username='manolo',
                                                first_name='Manuel',
                                                last_name='García García',
                                                is_active=False)

        friend = external_user_finder.find_friend(metrix_user_id=None, name='Manuel García García')

        self.assertEqual(friend.username, existing_friend.username)
        self.assertEqual(friend.slug, existing_friend.slug)
        self.assertEqual(friend.metrix_user_id, existing_friend.metrix_user_id)
        self.assertEqual(friend.first_name, 'Manuel')
        self.assertEqual(friend.last_name, 'García García')
        self.assertEqual(friend.is_active, False)

    def test_find_non_existing_friend(self):
        Friend.all_objects.all().delete()

        existing_friend = external_user_finder.find_friend(metrix_user_id='123', name='Manuel García García')

        self.assertEqual(existing_friend.username, 'manuel-garcia-garcia')
        self.assertEqual(existing_friend.metrix_user_id, '123')
        self.assertEqual(existing_friend.first_name, 'Manuel')
        self.assertEqual(existing_friend.last_name, 'García García')
        self.assertEqual(existing_friend.slug, 'manuel-garcia-garcia')
        self.assertEqual(existing_friend.is_active, False)

    def test_find_non_existing_friend_without_metrix_user_id(self):
        Friend.all_objects.all().delete()

        existing_friend = external_user_finder.find_friend(metrix_user_id=None, name='Manuel García García')

        self.assertEqual(existing_friend.username, 'manuel-garcia-garcia')
        self.assertEqual(existing_friend.metrix_user_id, None)
        self.assertEqual(existing_friend.first_name, 'Manuel')
        self.assertEqual(existing_friend.last_name, 'García García')
        self.assertEqual(existing_friend.slug, 'manuel-garcia-garcia')
        self.assertEqual(existing_friend.is_active, False)

    def test_find_non_existing_friend_with_similar_existing_friends(self):
        Friend.all_objects.all().delete()
        Friend.objects.create(username='manolo',
                              slug='manolo',
                              first_name='Manuel',
                              last_name='García García')
        Friend.objects.create(username='manolo2',
                              slug='manolo2',
                              first_name='Manuel',
                              last_name='García García')

        friend = external_user_finder.find_friend(metrix_user_id='123', name='Manuel García García')

        self.assertEqual(friend.username, 'manuel-garcia-garcia')
        self.assertEqual(friend.metrix_user_id, '123')
        self.assertEqual(friend.first_name, 'Manuel')
        self.assertEqual(friend.last_name, 'García García')
        self.assertEqual(friend.slug, 'manuel-garcia-garcia')
        self.assertEqual(friend.is_active, False)

    def test_find_non_existing_friend_with_similar_existing_friends_without_metrix_user_id(self):
        Friend.all_objects.all().delete()
        Friend.objects.create(username='manolo',
                              slug='manolo',
                              first_name='Manuel',
                              last_name='García García')
        Friend.objects.create(username='manolo2',
                              slug='manolo2',
                              first_name='Manuel',
                              last_name='García García')

        friend = external_user_finder.find_friend(metrix_user_id=None, name='Manuel García García')

        self.assertEqual(friend.username, 'manuel-garcia-garcia')
        self.assertEqual(friend.metrix_user_id, None)
        self.assertEqual(friend.first_name, 'Manuel')
        self.assertEqual(friend.last_name, 'García García')
        self.assertEqual(friend.slug, 'manuel-garcia-garcia')
        self.assertEqual(friend.is_active, False)

    def test_find_existing_friend_with_same_first_name_but_with_metrix_user_id(self):
        Friend.all_objects.all().delete()
        existing_friend = Friend.objects.create(metrix_user_id='123',
                                                username='johannes',
                                                slug='johannes',
                                                first_name='Johannes',
                                                last_name='Halaar',
                                                is_active=True)

        friend = external_user_finder.find_friend(metrix_user_id=None, name='Johannes')

        self.assertEqual(friend.username, existing_friend.username)
        self.assertEqual(friend.slug, existing_friend.slug)
        self.assertEqual(friend.metrix_user_id, existing_friend.metrix_user_id)
        self.assertEqual(friend.first_name, existing_friend.first_name)
        self.assertEqual(friend.last_name, existing_friend.last_name)
        self.assertEqual(friend.is_active, existing_friend.is_active)

    # Having a last name fixes the issue from the previous test
    def test_find_existing_friend_with_same_first_name_but_different_last_name(self):
        Friend.all_objects.all().delete()
        Friend.objects.create(metrix_user_id='123',
                              username='johannes',
                              slug='johannes',
                              first_name='Johannes',
                              last_name='Halaar',
                              is_active=True)

        friend = external_user_finder.find_friend(metrix_user_id=None, name='Johannes Dainat')

        self.assertEqual(friend.username, 'johannes-dainat')
        self.assertEqual(friend.slug, 'johannes-dainat')
        self.assertEqual(friend.metrix_user_id, None)
        self.assertEqual(friend.first_name, 'Johannes')
        self.assertEqual(friend.last_name, 'Dainat')
        self.assertEqual(friend.is_active, False)

    def test_find_existing_friend_with_same_first_name_but_different_metrix_user_id(self):
        Friend.all_objects.all().delete()
        existing_friend = Friend.objects.create(metrix_user_id='123',
                                                username='johannes',
                                                slug='johannes',
                                                first_name='Johannes',
                                                last_name='Halaar',
                                                is_active=True)

        friend = external_user_finder.find_friend(metrix_user_id='456', name='Johannes')

        self.assertEqual(friend.username, existing_friend.username)
        self.assertEqual(friend.slug, existing_friend.slug)
        self.assertEqual(friend.metrix_user_id, existing_friend.metrix_user_id)
        self.assertEqual(friend.first_name, existing_friend.first_name)
        self.assertEqual(friend.last_name, existing_friend.last_name)
        self.assertEqual(friend.is_active, existing_friend.is_active)

    # Having a last name fixes the issue from the previous test
    def test_find_existing_friend_with_same_first_name_but_different_metrix_user_id_and_last_name(self):
        Friend.all_objects.all().delete()
        Friend.objects.create(metrix_user_id='123',
                              username='johannes',
                              slug='johannes',
                              first_name='Johannes',
                              last_name='Halaar',
                              is_active=True)

        friend = external_user_finder.find_friend(metrix_user_id='456', name='Johannes Dainat')

        self.assertEqual(friend.username, 'johannes-dainat')
        self.assertEqual(friend.slug, 'johannes-dainat')
        self.assertEqual(friend.metrix_user_id, '456')
        self.assertEqual(friend.first_name, 'Johannes')
        self.assertEqual(friend.last_name, 'Dainat')
        self.assertEqual(friend.is_active, False)

    # Creating a non-active Friend in DB fixes the issue as well
    def test_find_2_existing_friends_with_same_first_name_but_different_metrix_user_id(self):
        Friend.all_objects.all().delete()
        Friend.objects.create(metrix_user_id='123',
                              username='johannes',
                              slug='johannes',
                              first_name='Johannes',
                              last_name='Halaar',
                              is_active=True)

        non_active_existing_friend = Friend.objects.create(metrix_user_id='456',
                                                           username='johannes-dainat',
                                                           slug='johannes-dainat',
                                                           first_name='Johannes',
                                                           last_name='Dainat',
                                                           is_active=False)

        friend = external_user_finder.find_friend(metrix_user_id='456', name='Johannes')

        self.assertEqual(friend.username, non_active_existing_friend.username)
        self.assertEqual(friend.slug, non_active_existing_friend.slug)
        self.assertEqual(friend.metrix_user_id, non_active_existing_friend.metrix_user_id)
        self.assertEqual(friend.first_name, non_active_existing_friend.first_name)
        self.assertEqual(friend.last_name, non_active_existing_friend.last_name)
        self.assertEqual(friend.is_active, non_active_existing_friend.is_active)
