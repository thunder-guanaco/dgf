import csv
import logging

import requests
from django.conf import settings
from django.core import management

from .models import Friend, Disc
from .pdga import PdgaApi

logger = logging.getLogger(__name__)


def fetch_pdga_data():
    logger.info('Fetching PDGA data...')

    pdga_api = PdgaApi()
    for friend in Friend.objects.all():
        pdga_api.update_friend_rating(friend)
        pdga_api.update_friend_tournament(friend)
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
