from django.test import TestCase

from ..apps import update_approved_discs
from ..models import Disc


class DiscModelsTest(TestCase):

    # assumption: if first, last, and one in the middle discs are properly loaded, then the rest too.
    def test_pd3_is_loaded(self):
        update_approved_discs()
        pd3 = Disc.objects.get(mold='PD3')
        self.assertEqual(pd3.mold, 'PD3')
        self.assertEqual(pd3.manufacturer, 'Discmania')

    def test_wham_o_is_loaded(self):
        update_approved_discs()
        pd3 = Disc.objects.get(
            mold='Professional (1, 4, 10, 14, 15, 16, 17, 20, 20 A, 21, 23A, 23B, 24A, 24B & Pro Classic molds)')
        self.assertEqual(pd3.mold,
                         'Professional (1, 4, 10, 14, 15, 16, 17, 20, 20 A, 21, '
                         '23A, 23B, 24A, 24B & Pro Classic molds)')
        self.assertEqual(pd3.manufacturer, 'Wham-O / DTW')

    def test_mirus_is_loaded(self):
        update_approved_discs()
        pd3 = Disc.objects.get(mold='Mirus')
        self.assertEqual(pd3.mold, 'Mirus')
        self.assertEqual(pd3.manufacturer, 'Latitude 64')
