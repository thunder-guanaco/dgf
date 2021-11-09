from django.test import TestCase

from .creator import create_friends
from ...models import DiscInBag, Disc


class DiscInBagModelTest(TestCase):

    def test_in_the_bag_and_representation(self):
        self.assert_in_the_bag_and_representation(expected_in_the_bag='2x FD',
                                                  expected_representation='2x FD (Fairway Driver)',
                                                  amount=2, mold='FD', type=DiscInBag.FAIRWAY_DRIVER)

        self.assert_in_the_bag_and_representation(expected_in_the_bag='Explorer',
                                                  expected_representation='Explorer (Fairway Driver)',
                                                  amount=1, mold='Explorer', type=DiscInBag.FAIRWAY_DRIVER)

    def assert_in_the_bag_and_representation(self, expected_in_the_bag, expected_representation, amount, mold, type):
        Disc.objects.all().delete()
        disc = Disc.objects.create(mold=mold)
        disc_in_bag = DiscInBag(friend=create_friends(1), amount=amount, disc=disc, type=type)
        self.assertEqual(disc_in_bag.in_the_bag, expected_in_the_bag)
        self.assertEqual(str(disc_in_bag), expected_representation)
