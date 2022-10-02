import logging
from datetime import datetime
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup
from django.db.models import Value
from django.db.models.functions import Replace

from dgf.models import Tournament, Friend
from dgf_cms.settings import GT_DATE_FORMAT, GT_LIST_PAGE, GT_DETAILS_PAGE, GT_RATING_PAGE

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

    ids = set()
    for tournament_tr in tournaments_table.findChildren(recursive=False):
        tournament_tds = tournament_tr.findChildren(recursive=False)
        url = tournament_tds[0].find('a')['href']
        ids.add(extract_gt_id(url))
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


def get_all_tournaments_from_ratings_page():
    tournament_ids = set()
    for friend in Friend.objects.filter(gt_number__isnull=False):
        player_page_soup = get(GT_RATING_PAGE.format(friend.gt_number))
        result_links = player_page_soup.findAll('a', title='GT Ergebnisse')
        for link in result_links:

            url = link['href']
            if 'turniere.discgolf.de' in url:
                tournament_id = extract_gt_id(url)
                tournament_ids.add(tournament_id)
            elif 'german-tour-online.de' in url:
                # we do not parse these URLS anymore since https://german-tour-online.de is not live anymore
                pass
            else:
                raise ValueError(f'Tournament URL not recognized: {url}')

    return tournament_ids


# ADD AND DELETE

def update_tournament(tournament, gt_id=None, pdga_id=None, name=None, begin=None, end=None):
    if gt_id:
        tournament.gt_id = gt_id
    if pdga_id:
        tournament.pdga_id = pdga_id
    if name:
        tournament.name = name
    if begin:
        tournament.begin = begin
    if end:
        tournament.end = end
    tournament.save()
    logger.info(f'Updated tournament {tournament} (GT={tournament.gt_id}, PDGA={tournament.pdga_id})')
    return tournament


def find_gt_tournament(gt_id):
    try:
        logger.info('Trying to find tournament by GT ID...')
        return Tournament.all_objects.get(gt_id=gt_id)
    except Tournament.DoesNotExist:
        return None


def find_pdga_tournament_by_name_and_date(name, begin, end):
    try:
        simple_name = name.replace(' ', '')
        logger.info('Trying to find tournament by name and date...')
        return (Tournament.all_objects.filter(pdga_id__isnull=False,
                                              begin=begin,
                                              end=end)
                .annotate(simple_name=Replace("name", Value(" "), Value("")))
                .get(simple_name__iexact=simple_name))  # Further steps like icontains should be done by humans...
    except Tournament.DoesNotExist:
        return None


def find_pdga_tournament(pdga_id, name, begin, end):
    try:
        logger.info('Trying to find tournament by PDGA ID...')
        return Tournament.all_objects.get(pdga_id__isnull=False,
                                          pdga_id=pdga_id)
    except Tournament.DoesNotExist:
        return find_pdga_tournament_by_name_and_date(name, begin, end)


def delete_pdga_tournament(tournament):
    tournament.delete()
    logger.info(f'Deleted PDGA tournament with PDGA ID = {tournament.pdga_id}')


def log_not_found_tournament(name, gt_id, pdga_id):
    logger.info(f'Tournament {name} was not found (GT: {gt_id}, PDGA: {pdga_id})')


def log_found_tournament(tournament, previous_import=''):
    message = f'Tournament already exists from previous {previous_import} import {tournament} '
    if previous_import == '':
        message += f'(GT: {tournament.gt_id}, PDGA: {tournament.pdga_id})'
    if previous_import == 'gt':
        message += f'(GT: {tournament.gt_id})'
    if previous_import == 'pdga':
        message += f'(PDGA: {tournament.pdga_id})'

    logger.info(message)


def add_or_update_tournament(gt_tournament):
    gt_id = gt_tournament['gt_id']
    name = gt_tournament['name']
    begin = datetime.strptime(gt_tournament['begin'], GT_DATE_FORMAT).date()
    end = datetime.strptime(gt_tournament['end'], GT_DATE_FORMAT).date()
    pdga_id = gt_tournament['pdga_id']

    existing_gt_tournament = find_gt_tournament(gt_id)
    existing_pdga_tournament = find_pdga_tournament(pdga_id, name, begin, end)

    if existing_gt_tournament:

        # GT + PDGA
        if existing_pdga_tournament:
            pdga_id = existing_pdga_tournament.pdga_id  # just in case the pdga_id is not set in gt_tournament
            if existing_gt_tournament.id == existing_pdga_tournament.id:
                log_found_tournament(existing_gt_tournament)
            else:
                log_found_tournament(existing_gt_tournament, previous_import='gt')
                log_found_tournament(existing_pdga_tournament, previous_import='pdga')
                # GT is the leading source
                delete_pdga_tournament(existing_pdga_tournament)
            tournament = update_tournament(existing_gt_tournament, pdga_id=pdga_id, name=name, begin=begin, end=end)

        # GT
        else:
            log_found_tournament(existing_gt_tournament, previous_import='gt')
            tournament = update_tournament(existing_gt_tournament, pdga_id=pdga_id, name=name, begin=begin, end=end)
    else:

        # PDGA
        if existing_pdga_tournament:
            log_found_tournament(existing_pdga_tournament, previous_import='pdga')
            tournament = update_tournament(existing_pdga_tournament, gt_id=gt_id, name=name, begin=begin, end=end)

        # not found
        else:
            log_not_found_tournament(name, gt_id, pdga_id)
            tournament = Tournament.objects.create(gt_id=gt_id, pdga_id=pdga_id, name=name, begin=begin, end=end)
            logger.info(f'Created tournament {tournament} (GT={tournament.gt_id}, PDGA={tournament.pdga_id})')

    return tournament


def delete_tournament(gt_tournament):
    deleted, _ = Tournament.all_objects.filter(gt_id=gt_tournament['gt_id']).delete()
    if deleted:
        logger.info(f'Deleted tournament with GT ID {gt_tournament["gt_id"]}: {gt_tournament["name"]}')


# OTHER COMMON FUNCTIONS

class ColumnNotFound(Exception):
    def __init__(self, text):
        self.text = text


def find_column(headers, text):
    for i, th in enumerate(headers.find_all('th')):
        if th.text == text:
            return i
    raise ColumnNotFound(text)
