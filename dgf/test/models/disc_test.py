from django.test import TestCase

from ...models import Disc


class DiscModelTest(TestCase):

    def test_display_name(self):
        self.expect_display_name(expected='FD', mold='FD (Jackal, Fairway Driver)')
        self.expect_display_name(expected='Explorer', mold='Explorer')

    def expect_display_name(self, expected, mold):
        disc = Disc.objects.create(mold=mold)
        self.assertEqual(disc.display_name, expected)
