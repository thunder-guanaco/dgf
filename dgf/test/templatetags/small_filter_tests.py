from django.test import TestCase

from dgf.models import Disc, DiscInBag, Friend
from dgf.templatetags.dgf import filter_by_type
from dgf.test.models.creator import create_friends, create_discs


class SmallFilterTests(TestCase):

    def setUp(self):
        Disc.objects.all().delete()
        Friend.objects.all().delete()

    def test_filter_discs_by_type(self):
        friend = create_friends(1)
        discs = create_discs(10)
        DiscInBag.objects.create(friend=friend, disc=discs[0], type=DiscInBag.PUTTER)
        DiscInBag.objects.create(friend=friend, disc=discs[1], type=DiscInBag.PUTTER)
        DiscInBag.objects.create(friend=friend, disc=discs[2], type=DiscInBag.PUTTER)
        DiscInBag.objects.create(friend=friend, disc=discs[3], type=DiscInBag.PUTTER)
        DiscInBag.objects.create(friend=friend, disc=discs[4], type=DiscInBag.MID_RANGE)
        DiscInBag.objects.create(friend=friend, disc=discs[5], type=DiscInBag.MID_RANGE)
        DiscInBag.objects.create(friend=friend, disc=discs[6], type=DiscInBag.MID_RANGE)
        DiscInBag.objects.create(friend=friend, disc=discs[7], type=DiscInBag.FAIRWAY_DRIVER)
        DiscInBag.objects.create(friend=friend, disc=discs[8], type=DiscInBag.FAIRWAY_DRIVER)
        DiscInBag.objects.create(friend=friend, disc=discs[9], type=DiscInBag.DISTANCE_DRIVER)

        self.assert_in_the_bag(friend, DiscInBag.PUTTER, discs[0:4])
        self.assert_in_the_bag(friend, DiscInBag.PUTTER, discs[4:7])
        self.assert_in_the_bag(friend, DiscInBag.PUTTER, discs[7:9])
        self.assert_in_the_bag(friend, DiscInBag.PUTTER, discs[9:])

    def assert_in_the_bag(self, friend, type, discs):
        in_the_bag = [disc_in_bag.disc.mold for disc_in_bag in filter_by_type(friend.discs.all(), type)]
        self.assertEqual(in_the_bag, discs)

    def test_filter_videos_by_type(self):
        friend = create_friends(1)
        video = create_videos(10)
        DiscInBag.objects.create(friend=friend, disc=discs[0], type=DiscInBag.PUTTER)
        DiscInBag.objects.create(friend=friend, disc=discs[1], type=DiscInBag.PUTTER)
        DiscInBag.objects.create(friend=friend, disc=discs[2], type=DiscInBag.PUTTER)
        DiscInBag.objects.create(friend=friend, disc=discs[3], type=DiscInBag.PUTTER)
        DiscInBag.objects.create(friend=friend, disc=discs[4], type=DiscInBag.MID_RANGE)
        DiscInBag.objects.create(friend=friend, disc=discs[5], type=DiscInBag.MID_RANGE)
        DiscInBag.objects.create(friend=friend, disc=discs[6], type=DiscInBag.MID_RANGE)
        DiscInBag.objects.create(friend=friend, disc=discs[7], type=DiscInBag.FAIRWAY_DRIVER)
        DiscInBag.objects.create(friend=friend, disc=discs[8], type=DiscInBag.FAIRWAY_DRIVER)
        DiscInBag.objects.create(friend=friend, disc=discs[9], type=DiscInBag.DISTANCE_DRIVER)

        self.assert_in_the_bag(friend, DiscInBag.PUTTER, discs[0:4])
        self.assert_in_the_bag(friend, DiscInBag.PUTTER, discs[4:7])
        self.assert_in_the_bag(friend, DiscInBag.PUTTER, discs[7:9])
        self.assert_in_the_bag(friend, DiscInBag.PUTTER, discs[9:])
