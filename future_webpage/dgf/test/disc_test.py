from django.conf import settings
from django.test import TestCase

from ..apps import update_approved_discs
from ..models import Disc


class DiscModelsTest(TestCase):

    # assumption: if first, last, and one in the middle discs are properly loaded, then the rest too.
    def test_pd3_is_loaded(self):
        Disc.objects.all().delete()
        update_approved_discs('{}/dgf/resources/test-pdga-approved-disc-golf-discs.csv'.format(settings.BASE_DIR))

        self.assertNotEqual(Disc.objects.get(mold='PD3', manufacturer='Discmania'), None)

        self.assertNotEqual(Disc.objects.get(
            mold='Professional (1, 4, 10, 14, 15, 16, 17, 20, 20 A, 21, 23A, 23B, 24A, 24B & Pro Classic molds)',
            manufacturer='Wham-O / DTW'), None)

        self.assertNotEqual(Disc.objects.get(mold='Mirus', manufacturer='Latitude 64'), None)

    def test_different_molds_are_loaded(self):
        Disc.objects.all().delete()
        update_approved_discs('{}/dgf/resources/test-pdga-approved-disc-golf-discs.csv'.format(settings.BASE_DIR))
        update_approved_discs(
            '{}/dgf/resources/test-more-molds-pdga-approved-disc-golf-discs.csv'.format(settings.BASE_DIR))

        self.assertNotEqual(Disc.objects.get(mold='PD3', manufacturer='Discmania'), None)

        self.assertNotEqual(Disc.objects.get(
            mold='Professional (1, 4, 10, 14, 15, 16, 17, 20, 20 A, 21, 23A, 23B, 24A, 24B & Pro Classic molds)',
            manufacturer='Wham-O / DTW'), None)

        self.assertNotEqual(Disc.objects.get(mold='Mirus', manufacturer='Latitude 64'), None)

        self.assertNotEqual(Disc.objects.get(mold='Torque', manufacturer='Discraft'), None)

        self.assertNotEqual(Disc.objects.get(mold='Pulse', manufacturer='Discraft'), None)
