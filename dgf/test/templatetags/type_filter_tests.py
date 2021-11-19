from django.test import TestCase

from dgf.models import Disc, DiscInBag, Friend, Video
from dgf.templatetags.dgf import filter_by_type
from dgf.test.models.creator import create_friends, create_discs


class TypeFilterTests(TestCase):

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
        self.assert_in_the_bag(friend, DiscInBag.MID_RANGE, discs[4:7])
        self.assert_in_the_bag(friend, DiscInBag.FAIRWAY_DRIVER, discs[7:9])
        self.assert_in_the_bag(friend, DiscInBag.DISTANCE_DRIVER, discs[9:])

    def test_filter_videos_by_type(self):
        friend = create_friends(1)
        videos = [
            Video.objects.create(friend=friend, url='http://example.com/video/0', type=Video.ACE),
            Video.objects.create(friend=friend, url='http://example.com/video/1', type=Video.ACE),
            Video.objects.create(friend=friend, url='http://example.com/video/2', type=Video.ACE),
            Video.objects.create(friend=friend, url='http://example.com/video/3', type=Video.IN_THE_BAG),
            Video.objects.create(friend=friend, url='http://example.com/video/4', type=Video.IN_THE_BAG),
            Video.objects.create(friend=friend, url='http://example.com/video/5', type=Video.OTHER),
        ]

        self.assert_videos(friend, Video.ACE, videos[0:3])
        self.assert_videos(friend, Video.IN_THE_BAG, videos[3:5])
        self.assert_videos(friend, Video.OTHER, videos[5:])

    def assert_in_the_bag(self, friend, type, expected_discs):
        molds = [disc_in_bag.disc.mold for disc_in_bag in filter_by_type(friend.discs.all(), type)]
        expected_molds = [disc.mold for disc in expected_discs]
        self.assertEqual(molds, expected_molds)

    def assert_videos(self, friend, type, expected_videos):
        urls = [video.url for video in filter_by_type(friend.videos.all(), type)]
        expected_urls = [video.url for video in expected_videos]
        self.assertEqual(urls, expected_urls)
