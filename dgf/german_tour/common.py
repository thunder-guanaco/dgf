import logging
from datetime import datetime
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

from dgf.models import Tournament
from dgf_cms.settings import GT_DATE_FORMAT

logger = logging.getLogger(__name__)


# GET AND EXTRACT FROM URLS

def get(url):
    logger.info(f'GET {url}')
    response = requests.get(url)
    return BeautifulSoup(response.content, features='html5lib')


def extract_gt_id(url):
    parsed_url = urlparse(url)
    parsed_query_params = parse_qs(parsed_url.query)
    return int(parsed_query_params['id'][0])


# ADD AND DELETE

def update_tournament(tournament, gt_id=None, name=None, begin=None, end=None):
    if gt_id:
        tournament.gt_id = gt_id
    if name:
        tournament.name = name
    if begin:
        tournament.begin = begin
    if end:
        tournament.end = end
    tournament.save()
    return tournament


def find_tournament_by_gt_id(gt_id):
    try:
        return Tournament.all_objects.get(gt_id=gt_id)
    except Tournament.DoesNotExist:
        return None


def find_pdga_tournament_by_name_and_date(name, begin, end):
    try:
        return Tournament.all_objects.get(name=name,
                                          begin=begin,
                                          end=end,
                                          pdga_id__isnull=False)
    except Tournament.DoesNotExist:
        return None


def add_tournament(gt_tournament):
    gt_id = gt_tournament['id']
    name = gt_tournament['name']
    begin = datetime.strptime(gt_tournament['begin'], GT_DATE_FORMAT)
    end = datetime.strptime(gt_tournament['end'], GT_DATE_FORMAT)

    tournament = find_tournament_by_gt_id(gt_id)
    if tournament is not None:
        logger.info(f'Tournament already exists from previous GT import {tournament} '
                    f'(PDGA={tournament.pdga_id}, GT={tournament.gt_id})')
        tournament = update_tournament(tournament, name=name, begin=begin, end=end)
        logger.info(f'Changed to: {tournament} (PDGA={tournament.pdga_id}, GT={tournament.gt_id})')
        return tournament

    tournament = find_pdga_tournament_by_name_and_date(name, begin, end)
    if tournament is not None:
        logger.info(f'Tournament already exists from previous PDGA import {tournament} '
                    f'(PDGA={tournament.pdga_id}, GT={tournament.gt_id})')
        tournament = update_tournament(tournament, gt_id=gt_id)
        logger.info(f'Changed to: {tournament} (PDGA={tournament.pdga_id}, GT={tournament.gt_id}')
        return tournament

    tournament = Tournament.objects.create(gt_id=gt_id, name=name, begin=begin, end=end)
    logger.info(f'Created tournament {tournament}')
    return tournament


def delete_tournament(gt_tournament):
    tournament_name = gt_tournament['name']  # shouldn't we use the ID?
    Tournament.all_objects.filter(name=tournament_name).delete()
    logger.info(f'Deleted tournament {tournament_name}')


# OTHER COMMON METHODS

class ColumnNotFound(Exception):
    def __init__(self, text):
        self.text = text


def find_column(headers, text):
    for i, th in enumerate(headers.find_all('th')):
        if th.text == text:
            return i
    raise ColumnNotFound(text)
