import csv
import logging

import requests
from django.conf import settings
from django.core import management

from .models import Friend, Disc

logger = logging.getLogger(__name__)


def fetch_pdga_data():
    logger.info('Fetching PDGA data...')

    for friend in Friend.objects.all():
        friend.save()

    logger.info('PDGA data has been updated')


def __download_approved_discs():
    response = requests.get(settings.APPROVED_DISCS_URL)
    return str(response.content, 'utf-8').replace('\r\n', '\n').split('\n')


def __update_discs(discs):
    loaded_discs = csv.DictReader(discs, delimiter=',')
    stored_discs = [x for x in Disc.objects.all().values_list('mold', flat=True)]

    amount = 0
    for disc in loaded_discs:
        if disc['Disc Model'] not in stored_discs:
            Disc.objects.create(mold=disc['Disc Model'],
                                manufacturer=disc['Manufacturer / Distributor'])
            amount += 1
    return amount


def update_approved_discs():
    logger.info('Updating new PDGA approved discs...')

    csv_list = __download_approved_discs()
    logger.info('Downloaded all approved discs from the PDGA')

    amount = __update_discs(csv_list)
    logger.info('{} discs have been updated'.format(amount))


def backup():
    logger.info('Starting back up...')

    management.call_command('dbbackup')
    logger.info('Database backup has been completed')

    management.call_command('mediabackup')
    logger.info('Media backup has been completed')
