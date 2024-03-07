import responses
from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from dgf.models import Disc


class UpdateApprovedDiscsTest(TestCase):

    def setUp(self):
        test_file = open(f'{settings.BASE_DIR}/dgf/resources/update_approved_discs_tests.csv')
        responses.add(responses.GET,
                      settings.APPROVED_DISCS_URL, body=test_file.read(),
                      status=200)
        Disc.objects.all().delete()

    @responses.activate
    def test_discs_are_created(self):

        self.assertAmountOfDiscs(0)

        call_command('update_approved_discs')

        self.assertAmountOfDiscs(4)
        # just get them, if they don't exist these calls will fail
        Disc.objects.get(manufacturer='Discmania', mold='PD3')
        Disc.objects.get(manufacturer='Wham-O / DTW', mold='Professional')
        Disc.objects.get(manufacturer='Latitude 64', mold='Mirus')

    @responses.activate
    def test_discs_are_added(self):

        Disc.objects.create(manufacturer='Discmania', mold='PD3')
        Disc.objects.create(manufacturer='Wham-O / DTW', mold='Professional')
        self.assertAmountOfDiscs(2)

        call_command('update_approved_discs')

        self.assertAmountOfDiscs(4)
        # just get them, if they don't exist these calls will fail
        Disc.objects.get(manufacturer='Discmania', mold='PD3')
        Disc.objects.get(manufacturer='Wham-O / DTW', mold='Professional')
        Disc.objects.get(manufacturer='Latitude 64', mold='Mirus')

    @responses.activate
    def test_disc_name_update(self):

        Disc.objects.create(manufacturer='Hobbysport', mold='Hobbysport putter')  # lowercase p
        self.assertAmountOfDiscs(1)

        call_command('update_approved_discs')

        self.assertAmountOfDiscs(4)
        # just get them, if they don't exist these calls will fail
        Disc.objects.get(manufacturer='Hobbysport', mold='Hobbysport Putter')  # uppercase P
        Disc.objects.get(manufacturer='Discmania', mold='PD3')
        Disc.objects.get(manufacturer='Wham-O / DTW', mold='Professional')
        Disc.objects.get(manufacturer='Latitude 64', mold='Mirus')

    def assertAmountOfDiscs(self, expected_amount_of_discs):
        self.assertEqual(Disc.objects.all().count(), expected_amount_of_discs)
