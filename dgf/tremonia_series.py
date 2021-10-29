import logging
from datetime import datetime

import requests

from dgf.models import Tournament

logger = logging.getLogger(__name__)

DISC_GOLF_METRIX_COMPETITION_ENDPOINT = 'https://discgolfmetrix.com/api.php?content=result&id={}'
TREMONIA_SERIES_ID = '715021'


def build_url(id):
    return DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(id)


def get_tournament(id):
    url = build_url(id)
    logger.info(f'GET {url}')
    return requests.get(url).json()['Competition']


def extract_name(ts_tournament):
    return ts_tournament['Name'].split(' &rarr; ')[1]


def add_tournament(ts_tournament):
    date = datetime.strptime(ts_tournament['Date'], '%Y-%m-%d')

    tournament, created = Tournament.objects.get_or_create(name=extract_name(ts_tournament),
                                                           defaults={
                                                               'begin': date,
                                                               'end': date,
                                                               'url': build_url(ts_tournament['ID'])
                                                           })
    if created:
        logger.info(f'Created tournament {tournament}')


def create_tournament(id):
    tournament = get_tournament(id)
    add_tournament(tournament)


def update_tournaments():
    tournament = get_tournament(TREMONIA_SERIES_ID)
    for event in tournament['Events']:
        if not event['Name'].startswith('[DELETED]'):
            create_tournament(event['ID'])
