import logging
from datetime import datetime

import requests

from dgf import external_user_finder
from dgf.models import Tournament, Result, Attendance, Tour

logger = logging.getLogger(__name__)

DISC_GOLF_METRIX_COMPETITION_ENDPOINT = 'https://discgolfmetrix.com/api.php?content=result&id={}'
DISC_GOLF_METRIX_TOURNAMENT_PAGE = 'https://discgolfmetrix.com/{}'
TREMONIA_SERIES_ROOT_ID = '715021'
DISC_GOLF_METRIX_DATE_FORMAT = '%Y-%m-%d'


def get_tournament(id):
    url = DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(id)
    logger.info(f'GET {url}')
    return requests.get(url).json()['Competition']


def extract_name(ts_tournament):
    return ts_tournament['Name'].split(' &rarr; ')[1]


def get_results(ts_tournament):
    if 'TourResults' in ts_tournament:
        return ts_tournament['TourResults']
    else:
        return ts_tournament['SubCompetitions'][0]['Results']


def get_position(ts_result):
    try:
        return ts_result['Place']
    except KeyError:
        return ts_result['OrderNumber']


def add_attendance(tournament, ts_tournament):
    for ts_result in get_results(ts_tournament):
        friend = external_user_finder.find_friend(ts_result['UserID'], ts_result['Name'])
        logger.info(f'Using Friend: {friend}')
        _, created = Attendance.objects.get_or_create(friend=friend, tournament=tournament)
        if created:
            logger.info(f'Added attendance of {friend} to {tournament}\n')


def add_results(tournament, ts_tournament):
    for ts_result in get_results(ts_tournament):
        friend = external_user_finder.find_friend(ts_result['UserID'], ts_result['Name'])
        logger.info(f'Using Friend: {friend}')
        Result.objects.create(tournament=tournament,
                              friend=friend,
                              position=get_position(ts_result))
        logger.info(f'Added result of {friend} to {tournament}\n')


def add_tournament(ts_tournament):
    name = extract_name(ts_tournament)
    date = datetime.strptime(ts_tournament['Date'], DISC_GOLF_METRIX_DATE_FORMAT)
    id = ts_tournament['ID']

    tournament, created = Tournament.objects.get_or_create(metrix_id=id,
                                                           defaults={
                                                               'name': name,
                                                               'url': DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(id),
                                                               'begin': date,
                                                               'end': date,
                                                               'point_system': Tournament.TS_POINTS_WITH_BEATEN_PLAYERS,
                                                           })

    if created:
        logger.info(f'Created tournament {tournament}\n')
    else:
        # Always update. With Corona you never know
        tournament.name = name
        tournament.url = DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(id)
        tournament.begin = date
        tournament.end = date
        tournament.save()

    return tournament


def add_tours(tournament):
    # default tour containing all Tremonia Series
    default_tour, _ = Tour.objects.get_or_create(name='Ewige Tabelle',
                                                 defaults={'evaluate_how_many': 10000})
    tournament.tours.add(default_tour)

    # tournament year's tour
    years_tour, _ = Tour.objects.get_or_create(name=f'Tremonia Series {tournament.begin.year}',
                                               defaults={'evaluate_how_many': 6})
    tournament.tours.add(years_tour)


def create_tournament(metrix_id):
    ts_tournament = get_tournament(metrix_id)
    tournament = add_tournament(ts_tournament)
    add_tours(tournament)

    # tournament is either not played yet or still in play
    if tournament.begin >= datetime.today():
        add_attendance(tournament, ts_tournament)

    # tournament was already played and does not have results
    elif tournament.results.count() == 0:
        add_results(tournament, ts_tournament)
        tournament.re_calculate_points()


def update_tournaments():
    tournament = get_tournament(TREMONIA_SERIES_ROOT_ID)
    for event in tournament['Events']:
        if not event['Name'].startswith('[DELETED]'):
            logger.info('--------------------------------------------------------------------------------\n')
            create_tournament(event['ID'])
