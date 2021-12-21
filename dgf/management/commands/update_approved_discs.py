import csv
import logging

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from dgf.management import error_handler
from dgf.models import Disc

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Updates new PDGA approved discs'

    def download_approved_discs(self):
        response = requests.get(settings.APPROVED_DISCS_URL)
        return str(response.content, 'utf-8').replace('\r\n', '\n').split('\n')

    def update_discs(self, discs):
        loaded_discs = csv.DictReader(discs, delimiter=',')
        stored_discs = [x for x in Disc.objects.all().values_list('mold', flat=True)]

        amount = 0
        for disc in loaded_discs:
            if disc['Disc Model'] not in stored_discs:
                Disc.objects.create(mold=disc['Disc Model'],
                                    manufacturer=disc['Manufacturer / Distributor'])
                amount += 1
        return amount

    def handle(self, *args, **options):

        try:
            logger.info('Updating new PDGA approved discs...')

            csv_list = self.download_approved_discs()
            logger.info('Downloaded all approved discs from the PDGA')

            amount = self.update_discs(csv_list)
            logger.info(f'{amount} discs have been updated')

        except Exception as e:
            error_handler.handle(self, e)
