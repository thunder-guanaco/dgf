import csv
import logging

import requests
from django.conf import settings

from dgf.management.base_dgf_command import BaseDgfCommand
from dgf.models import Disc

logger = logging.getLogger(__name__)


class Command(BaseDgfCommand):
    help = 'Updates new PDGA approved discs'

    def download_approved_discs(self):
        response = requests.get(settings.APPROVED_DISCS_URL)
        return str(response.content, 'utf-8').replace('\r\n', '\n').split('\n')

    def update_discs(self, discs):
        loaded_discs = csv.DictReader(discs, delimiter=',')
        stored_discs = [x for x in Disc.objects.all().values_list('mold', flat=True)]

        amount = 0
        for disc in loaded_discs:
            mold = disc['Disc Model']
            if mold not in stored_discs:
                Disc.objects.update_or_create(mold__iexact=mold,
                                              manufacturer=disc['Manufacturer / Distributor'],
                                              defaults={'mold': mold})
                amount += 1
        return amount

    def run(self, *args, **options):

        csv_list = self.download_approved_discs()
        logger.info('Downloaded all approved discs from the PDGA')

        amount = self.update_discs(csv_list)
        logger.info(f'{amount} discs have been updated')
