import logging
from datetime import datetime
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

from dgf.models import Tournament
from dgf_cms.settings import GT_DATE_FORMAT, GT_LIST_PAGE, GT_DETAILS_PAGE

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


def extract_pdga_id(url):
    return int(url.split('/')[-1])


def get_all_tournaments_from_list_page():
    soup = get(GT_LIST_PAGE)
    tournaments_table = soup.find('table', id='list_tournaments').find('tbody')

    ids = []
    for tournament_tr in tournaments_table.findChildren(recursive=False):
        tournament_tds = tournament_tr.findChildren(recursive=False)
        url = tournament_tds[0].find('a')['href']
        ids.append(extract_gt_id(url))
    return ids


def parse_tournament_from_details_page(tournament_id):
    tournament_soup = get(GT_DETAILS_PAGE.format(tournament_id))
    dates = [d.strip() for d in tournament_soup.find('td', text='Turnierbetrieb').parent()[1].text.strip().split('-')]
    pdga_status = tournament_soup.find('td', text='PDGA Status').parent()[1].find('a')
    badge = tournament_soup.find('h2').find('i')
    return {
        'gt_id': tournament_id,
        'name': tournament_soup.find('h2').text.strip(),
        'begin': dates[0],
        'end': dates[1] if len(dates) > 1 else dates[0],
        'pdga_id': extract_pdga_id(pdga_status['href']) if pdga_status else None,
        'canceled': badge is not None and badge.text.strip() == 'ABGESAGT',
    }


# ADD AND DELETE

def update_tournament(tournament, gt_id=None, name=None, begin=None, end=None, pdga_id=None):
    if gt_id:
        tournament.gt_id = gt_id
    if name:
        tournament.name = name
    if begin:
        tournament.begin = begin
    if end:
        tournament.end = end
    if pdga_id:
        tournament.pdga_id = pdga_id
    tournament.save()
    return tournament


def find_tournament_by_gt_id(gt_id):
    try:
        logger.info('Trying to find tournament by GT ID...')
        return Tournament.all_objects.get(gt_id=gt_id)
    except Tournament.DoesNotExist:
        return None


def find_pdga_tournament_by_pdga_id(pdga_id):
    try:
        logger.info('Trying to find tournament by PDGA ID...')
        return Tournament.all_objects.get(pdga_id=pdga_id)
    except Tournament.DoesNotExist:
        return None


def find_pdga_tournament_by_name_and_date(name, begin, end):
    try:
        logger.info('Trying to find tournament by name and date...')
        return Tournament.all_objects.get(name=name,
                                          begin=begin,
                                          end=end,
                                          pdga_id__isnull=False)
    except Tournament.DoesNotExist:
        return None


def add_tournament(gt_tournament):
    gt_id = gt_tournament['gt_id']
    name = gt_tournament['name']
    begin = datetime.strptime(gt_tournament['begin'], GT_DATE_FORMAT)
    end = datetime.strptime(gt_tournament['end'], GT_DATE_FORMAT)
    pdga_id = gt_tournament['pdga_id']

    tournament = find_tournament_by_gt_id(gt_id)
    if tournament is not None:
        logger.info(f'Tournament already exists from previous GT import {tournament} '
                    f'(PDGA={tournament.pdga_id}, GT={tournament.gt_id})')
        tournament = update_tournament(tournament, name=name, begin=begin, end=end, pdga_id=pdga_id)
        logger.info(f'Changed to: {tournament} (PDGA={tournament.pdga_id}, GT={tournament.gt_id})')
        return tournament

    tournament = find_pdga_tournament_by_pdga_id(pdga_id)
    if tournament is None:
        tournament = find_pdga_tournament_by_name_and_date(name, begin, end)
    if tournament is not None:
        logger.info(f'Tournament already exists from previous PDGA import {tournament} '
                    f'(PDGA={tournament.pdga_id}, GT={tournament.gt_id})')
        tournament = update_tournament(tournament, gt_id=gt_id)
        logger.info(f'Changed to: {tournament} (PDGA={tournament.pdga_id}, GT={tournament.gt_id}')
        return tournament

    tournament = Tournament.objects.create(gt_id=gt_id, name=name, begin=begin, end=end, pdga_id=pdga_id)
    logger.info(f'Created tournament {tournament} (PDGA={tournament.pdga_id}, GT={tournament.gt_id})')
    return tournament


def delete_tournament(gt_tournament):
    amount, _ = Tournament.all_objects.filter(gt_id=gt_tournament['gt_id']).delete()
    if amount:
        logger.info(f'Deleted tournament with GT ID {gt_tournament["gt_id"]}: {gt_tournament["name"]}')


# OTHER COMMON METHODS

class ColumnNotFound(Exception):
    def __init__(self, text):
        self.text = text


def find_column(headers, text):
    for i, th in enumerate(headers.find_all('th')):
        if th.text == text:
            return i
    raise ColumnNotFound(text)
