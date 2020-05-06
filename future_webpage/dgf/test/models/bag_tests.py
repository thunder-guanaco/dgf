from django.test import TestCase

from ...models import Friend, DiscInBag, Disc


class DiscInBagModelTest(TestCase):

    def test_representation(self):
        self.expect_representation(expected='2x FD',
                                   amount=2, disc_mold='FD')

        self.expect_representation(expected='Explorer',
                                   amount=1, disc_mold='Explorer')

    def expect_representation(self, expected, amount, disc_mold):
        Friend.objects.all().delete()
        friend = Friend.objects.create(username='friend')
        disc = Disc.objects.create(mold=disc_mold)
        disc_in_bag = DiscInBag.objects.create(amount=amount, disc=disc, friend=friend)
        self.assertEqual(disc_in_bag.in_the_bag, expected)
