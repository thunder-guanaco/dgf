import logging
from datetime import datetime
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

from dgf.models import Tournament, Friend, Attendance, Result, Division
from dgf_cms.settings import TOURNAMENT_LIST_PAGE, GT_DATE_FORMAT, TOURNAMENT_ATTENDANCE_PAGE, TOURNAMENT_RESULTS_PAGE, \
    RATINGS_PAGE, TOURNAMENT_PAGE

logger = logging.getLogger(__name__)


def get(url):
    logger.info(f'GET {url}')
    return BeautifulSoup(requests.get(url).content, features='html5lib')


def get_all_tournaments():
    soup = get(TOURNAMENT_LIST_PAGE)
    tournaments_table = soup.find('table', id='list_tournaments').find('tbody')

    tournaments = []
    for tournament_tr in tournaments_table.findChildren(recursive=False):
        tournament_tds = tournament_tr.findChildren(recursive=False)
        badge = tournament_tds[0].find('h6')
        tournaments.append({
            'id': tournament_tds[0].find('a')['href'].split('=')[-1],
            'name': tournament_tds[0].find('a').text.strip(),
            'begin': tournament_tds[2].find('a').text.strip(),
            'end': tournament_tds[3].find('a').text.strip(),
            'canceled': badge is not None and badge.text.strip() == 'ABGESAGT',
        })

    return tournaments


def delete_tournament(gt_tournament):
    tournament_name = gt_tournament['name']
    Tournament.all_objects.filter(name=tournament_name).delete()
    logger.info(f'Deleted tournament {tournament_name}')


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


def find_column(headers, text):
    for i, th in enumerate(headers.find_all('th')):
        if th.text == text:
            return i
    return None


def parse_gt_numbers(attendance_header, attendance_content):
    gt_numbers = []
    gt_number_i = find_column(attendance_header, 'GT#')
    for tr in attendance_content.find_all('tr'):
        text = tr.find_all('td')[gt_number_i].text
        if text:
            gt_numbers.append(int(text))
    return gt_numbers


def add_attendance(gt_tournament, tournament):
    attendance_soup = get(TOURNAMENT_ATTENDANCE_PAGE.format(gt_tournament['id']))
    attendance_table = attendance_soup.find('table', id='starterlist')
    table_header = attendance_table.find('thead')
    table_content = attendance_table.find('tbody')

    if 'Keine Daten in der Tabelle vorhanden' in [td.text.strip() for td in table_content.find_all('td')]:
        logger.info(f'No attendance list for tournament {tournament}')
        return

    gt_numbers = parse_gt_numbers(table_header, table_content)
    for friend in Friend.objects.filter(gt_number__in=gt_numbers):
        _, created = Attendance.objects.get_or_create(friend=friend, tournament=tournament)
        if created:
            logger.info(f'Added attendance of {friend} to {tournament}')


def update_tournaments():
    gt_tournaments = get_all_tournaments()
    for gt_tournament in gt_tournaments:
        if gt_tournament['canceled']:
            delete_tournament(gt_tournament)
        elif gt_tournament['name'].startswith('Tremonia Series #'):
            logger.info(f'Ignoring tournament: {gt_tournament["name"]}. '
                        f'Tremonia Series tournaments are handled separately')
        else:
            tournament = add_tournament(gt_tournament)
            add_attendance(gt_tournament, tournament)


def create_result(friend, tournament, position, division):
    result, created = Result.objects.get_or_create(tournament=tournament,
                                                   friend=friend,
                                                   defaults={'position': position})

    result.division = division  # update division (some results might not have one)
    result.save()

    if created:
        logger.info(f'Added result: {result}')


def get_turniere_discgolf_de_id(url):
    parsed_url = urlparse(url)
    parsed_query_params = parse_qs(parsed_url.query)
    return int(parsed_query_params['id'][0])


def get_german_tour_online_id(url):
    return url.split('/')[-1]


def parse_gt_number(gt_number_text):
    return int(gt_number_text) if gt_number_text.strip() else None


DIVISION_MAPPING = {
    'O': 'MPO',
    'W': 'FPO',
    'M40': 'MP40',
    'M50': 'MP50',
    'M60': 'MP60',
    'M70': 'MP70',
    'WM40': 'FP40',
}


def parse_division(division_text):
    division_text = division_text.strip()
    division_id = DIVISION_MAPPING.get(division_text, division_text)
    try:
        return Division.objects.get(id=division_id)
    except Division.DoesNotExist as e:
        logger.error(f'Division {division_text} does not exist')
        raise e


def parse_position(position_text):
    if 'DNF' in position_text:
        return 'DNF'

    return int(position_text)


def parse_turniere_discgolf_de_table_results(results_header, results_content, tournament):
    gt_number_i = find_column(results_header, 'GT#')
    division_i = find_column(results_header, 'Division ')
    position_i = find_column(results_header, '#')
    for tr in results_content.find_all('tr'):

        gt_number = parse_gt_number(tr.find_all('td')[gt_number_i].text)
        if not gt_number:
            continue

        division = parse_division(tr.find_all('td')[division_i].text)
        position = parse_position(tr.find_all('td')[position_i].text)
        try:
            friend = Friend.objects.get(gt_number=gt_number)
            create_result(friend, tournament, position, division)
        except Friend.DoesNotExist:
            pass  # it's not a Friend, ignore them


def parse_turniere_discgolf_de_tournament(tournament_id):
    tournament_soup = get(TOURNAMENT_PAGE.format(tournament_id))
    dates = [d.strip() for d in tournament_soup.find("td", text="Turnierbetrieb").parent()[1].text.strip().split("-")]
    return {
        'id': tournament_id,
        'name': tournament_soup.find('h2').text.strip(),
        'begin': dates[0],
        'end': dates[1] if len(dates) > 1 else dates[0]
    }


# TODO: #3090
def parse_german_tour_online_tournament(tournament_id):
    return None


def parse_turniere_discgolf_de_results(tournament, tournament_id):
    results_soup = get(TOURNAMENT_RESULTS_PAGE.format(tournament_id))

    results_tables = results_soup.find_all('table')
    for results_table in results_tables:
        table_header = results_table.find('thead')
        table_content = results_table.find('tbody')
        parse_turniere_discgolf_de_table_results(table_header, table_content, tournament)


# TODO: #3090
def parse_german_tour_online_results(tournament, url):
    pass


def add_tournament_result(url, get_id_from_url, parse_tournament, parse_results):
    tournament_id = get_id_from_url(url)
    gt_tournament = parse_tournament(tournament_id)
    tournament = add_tournament(gt_tournament)
    parse_results(tournament, tournament_id)


def get_all_result_urls():
    urls = set()
    for friend in Friend.objects.filter(gt_number__isnull=False):
        player_page_soup = get(RATINGS_PAGE.format(friend.gt_number))
        result_links = player_page_soup.findAll('a', text='GT Ergebnisse')
        for link in result_links:
            urls.add(link['href'])

    return urls


def update_tournament_results():
    for url in get_all_result_urls():

        logger.info('\n-------------------------------------------')

        if 'turniere.discgolf.de' in url:
            add_tournament_result(url,
                                  get_turniere_discgolf_de_id,
                                  parse_turniere_discgolf_de_tournament,
                                  parse_turniere_discgolf_de_results)

        elif 'german-tour-online.de' in url:
            logger.info(f'(still) ignoring tournaments from german-tour-online.de: {url}')
            # TODO: #3090
            # add_tournament_result(url,
            #                       get_german_tour_online_id,
            #                       parse_german_tour_online_tournament,
            #                       parse_german_tour_online_results)

        else:
            raise ValueError(f'Tournament URL not recognized: {url}')
