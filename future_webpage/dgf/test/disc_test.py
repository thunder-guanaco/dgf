import responses
from django.conf import settings
from django.test import TestCase

from ..cronjobs import update_approved_discs_cron
from ..models import Disc


def configure_response(param):
    responses.add(responses.GET,
                  settings.APPROVED_DISCS_URL, body=param.read(),
                  status=200)


class DiscModelsTest(TestCase):

    @responses.activate
    def test_three_discs_are_loaded(self):
        configure_response(open('{}/dgf/resources/test-pdga-approved-disc-golf-discs.csv'.format(settings.BASE_DIR)))
        Disc.objects.all().delete()
        update_approved_discs_cron()
        self.assertNotEqual(Disc.objects.get(mold='PD3', manufacturer='Discmania'), None)

        self.assertNotEqual(Disc.objects.get(
            mold='Professional (1, 4, 10, 14, 15, 16, 17, 20, 20 A, 21, 23A, 23B, 24A, 24B & Pro Classic molds)',
            manufacturer='Wham-O / DTW'), None)

        self.assertNotEqual(Disc.objects.get(mold='Mirus', manufacturer='Latitude 64'), None)

    @responses.activate
    def test_different_molds_are_loaded(self):
        configure_response(
            open('{}/dgf/resources/test-more-molds-pdga-approved-disc-golf-discs.csv'.format(settings.BASE_DIR)))

        Disc.objects.all().delete()
        update_approved_discs_cron()

        self.assertNotEqual(Disc.objects.get(mold='PD3', manufacturer='Discmania'), None)

        self.assertNotEqual(Disc.objects.get(
            mold='Professional (1, 4, 10, 14, 15, 16, 17, 20, 20 A, 21, 23A, 23B, 24A, 24B & Pro Classic molds)',
            manufacturer='Wham-O / DTW'), None)

        self.assertNotEqual(Disc.objects.get(mold='Mirus', manufacturer='Latitude 64'), None)

        self.assertNotEqual(Disc.objects.get(mold='Torque', manufacturer='Discraft'), None)

        self.assertNotEqual(Disc.objects.get(mold='Pulse', manufacturer='Discraft'), None)
