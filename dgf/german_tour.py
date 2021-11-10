import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from dgf.models import Tournament, Friend, Attendance

logger = logging.getLogger(__name__)

TOURNAMENT_LIST_PAGE = 'https://turniere.discgolf.de/index.php?p=events'
TOURNAMENT_PAGE = 'https://turniere.discgolf.de/index.php?p=events&sp=view&id={}'
TOURNAMENT_ATTENDANCE_PAGE = 'https://turniere.discgolf.de/index.php?p=events&sp=list-players&id={}'

GT_DATE_FORMAT = '%d.%m.%Y'


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
    Tournament.objects.filter(name=tournament_name).delete()
    logger.info(f'Deleted tournament {tournament_name}')


def add_tournament(gt_tournament):
    begin_date = datetime.strptime(gt_tournament['begin'], GT_DATE_FORMAT)
    end_date = datetime.strptime(gt_tournament['end'], GT_DATE_FORMAT)

    tournament, created = Tournament.objects.get_or_create(gt_id=gt_tournament['id'],
                                                           defaults={
                                                               'name': gt_tournament['name'],
                                                               'url': TOURNAMENT_PAGE.format(gt_tournament['id']),
                                                               'begin': begin_date,
                                                               'end': end_date,
                                                           })
    if created:
        logger.info(f'Created tournament {tournament}')
    else:
        # Always update the date. With Corona you never know
        tournament.begin = begin_date
        tournament.end = end_date
        tournament.save()

    return tournament


def find_gt_number_column(attendance_headers):
    for i, th in enumerate(attendance_headers.find_all('th')):
        if th.text == 'GT#':
            logger.info(f'Found GT# header at position {i}')
            return i


def parse_gt_numbers(attendance_header, attendance_content):
    gt_numbers = []
    gt_number_i = find_gt_number_column(attendance_header)
    for tr in attendance_content.find_all('tr'):
        text = tr.find_all('td')[gt_number_i].text
        if text:
            gt_numbers.append(int(text))
    return gt_numbers


def add_attendance(tournament, attendance_soup):
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
            attendance_soup = get(TOURNAMENT_ATTENDANCE_PAGE.format(gt_tournament['id']))
            add_attendance(tournament, attendance_soup)
