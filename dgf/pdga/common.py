import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from dgf.models import Tournament
from dgf_cms.settings import PDGA_DATE_FORMAT, PDGA_PAGE_BASE_URL

logger = logging.getLogger(__name__)


# GET AND EXTRACT FROM URLS

def get_page(url):
    url = f'{PDGA_PAGE_BASE_URL}{url}'
    logger.info(f'Getting {url}')
    return BeautifulSoup(requests.get(url).content, features='html5lib')


def get_player_page(pdga_number):
    return get_page(f'/player/{pdga_number}')


# ADD

def add_tournament(pdga_api, pdga_id):
    pdga_tournament = pdga_api.get_event(tournament_id=pdga_id)
    begin_date = datetime.strptime(pdga_tournament['start_date'], PDGA_DATE_FORMAT)
    end_date = datetime.strptime(pdga_tournament['end_date'], PDGA_DATE_FORMAT)

    tournament, created = Tournament.all_objects.get_or_create(pdga_id=pdga_tournament['tournament_id'],
                                                               defaults={
                                                                   'name': pdga_tournament['tournament_name'],
                                                                   'begin': begin_date,
                                                                   'end': end_date
                                                               })
    if created:
        logger.info(f'Created tournament {tournament}')
    else:
        # Always update. With Corona you never know
        tournament.name = pdga_tournament['tournament_name']
        tournament.begin = begin_date
        tournament.end = end_date
        tournament.save()

    return tournament
