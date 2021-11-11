from django.test import TestCase

from ...models import Disc


class DiscModelTest(TestCase):

    def test_representation(self):
        disc = Disc(mold='FD', manufacturer='Discmania')
        self.assertEqual(str(disc), 'FD [Discmania]')

    def test_display_name(self):
        self.assert_display_name(expected='FD', mold='FD (Jackal, Fairway Driver)')
        self.assert_display_name(expected='Explorer', mold='Explorer')

    def assert_display_name(self, expected, mold):
        Disc.objects.all().delete()
        disc = Disc.objects.create(mold=mold)
        self.assertEqual(disc.display_name, expected)
