import uuid

from django.test import TestCase

from dgf.cms_plugins import unassigned_bag_tags
from dgf.models import Friend


class BagTags(TestCase):

    def test_unassigned_bag_tags(self):
        self.assert_that(having_bag_tags=[1, 2, 3, 4, 5],
                         expect_unassigned_bag_tags=[])

        self.assert_that(having_bag_tags=[],
                         expect_unassigned_bag_tags=[])

        self.assert_that(having_bag_tags=[1, 3, 4, 5],
                         expect_unassigned_bag_tags=[2])

        self.assert_that(having_bag_tags=[1, 3, 5],
                         expect_unassigned_bag_tags=[2, 4])

        self.assert_that(having_bag_tags=[3, 4, 5],
                         expect_unassigned_bag_tags=[1, 2])

    def assert_that(self, having_bag_tags, expect_unassigned_bag_tags):
        Friend.objects.all().delete()

        for bag_tag in having_bag_tags:
            Friend.objects.create(username=uuid.uuid4(), bag_tag=bag_tag)

        self.assertEqual(unassigned_bag_tags(), expect_unassigned_bag_tags)
