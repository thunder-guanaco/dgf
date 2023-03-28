import logging
from datetime import datetime

import requests

from dgf import external_user_finder
from dgf.models import Tournament, Result, Attendance, Tour, Division
from dgf_cms.settings import DISC_GOLF_METRIX_COMPETITION_ENDPOINT, DISC_GOLF_METRIX_DATE_FORMAT, \
    TREMONIA_SERIES_ROOT_ID

logger = logging.getLogger(__name__)


TS_DIVISIONS = {
    'Open': 'MPO',
    'Amateur': 'MA4',
}


def get_tournament(id):
    url = DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(id)
    logger.info(f'GET {url}')
    return requests.get(url).json()['Competition']


def extract_name(ts_tournament):
    return ts_tournament['Name'].split(' &rarr; ')[1]


def get_results(ts_tournament):
    try:
        return ts_tournament['TourResults']
    except KeyError:
        return ts_tournament['SubCompetitions'][0]['Results']


def get_position(ts_result):
    try:
        return ts_result['Place']
    except KeyError:
        return ts_result['OrderNumber']


def get_division(ts_result):
    ts_class = ts_result.get('ClassName') or 'Open'
    return Division.objects.get(id=TS_DIVISIONS[ts_class])


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
        result = Result.objects.create(tournament=tournament,
                                       friend=friend,
                                       position=get_position(ts_result),
                                       division=get_division(ts_result))
        logger.info(f'Added result: {result}')


def add_or_update_tournament(ts_tournament):
    name = extract_name(ts_tournament)
    date = datetime.strptime(ts_tournament['Date'], DISC_GOLF_METRIX_DATE_FORMAT)
    id = ts_tournament['ID']

    tournament, created = Tournament.objects.get_or_create(metrix_id=id,
                                                           defaults={
                                                               'name': name,
                                                               'begin': date,
                                                               'end': date,
                                                               'point_system': Tournament.TS_POINTS_WITH_BEATEN_PLAYERS,
                                                           })

    if created:
        logger.info(f'Created tournament {tournament}\n')
    else:
        # Always update, the dates might have changed and the name changes after the tournament
        tournament.name = name
        tournament.begin = date
        tournament.end = date
        tournament.save()

    return tournament


def add_tours(tournament):
    divisions = tournament.results.filter(division__isnull=False).values_list('division', flat=True).distinct()

    if not divisions:
        logger.info(f'Skipping adding tours to {tournament.name} because it has no results (and no divisions)')
        return

    # default tour containing all Tremonia Series
    add_to_tour('Ewige Tabelle', tournament, divisions)

    # tournament year's tour
    add_to_tour(f'Tremonia Series {tournament.begin.year}', tournament, divisions, evaluate_how_many=7)


def add_to_tour(name, tournament, divisions, evaluate_how_many=10000):
    for division in divisions:
        tour, created = Tour.objects.get_or_create(name=name,
                                                   division=Division.objects.get(id=division),
                                                   defaults={'evaluate_how_many': evaluate_how_many})

        if created:
            logger.info(f'Created Tour: {tour}')

        tournament.tours.add(tour)
        logger.info(f'Added {tournament} to {tour}')


def create_or_update_tournament(metrix_id):
    ts_tournament = get_tournament(metrix_id)
    tournament = add_or_update_tournament(ts_tournament)

    # tournament is either not played yet or still in play
    if tournament.begin >= datetime.today():
        add_attendance(tournament, ts_tournament)

    # tournament was already played and does not have results
    elif tournament.results.count() == 0:
        add_results(tournament, ts_tournament)
        tournament.recalculate_points()

    add_tours(tournament)


def update_tournaments():
    tournament = get_tournament(TREMONIA_SERIES_ROOT_ID)
    for event in tournament['Events']:
        if not event['Name'].startswith('[DELETED]'):
            logger.info('\n')
            create_or_update_tournament(event['ID'])
            logger.info('--------------------------------------------------------------------------------')


def next_tournaments():
    return Tournament.objects.filter(name__startswith='Tremonia Series') \
        .filter(begin__gte=datetime.today()) \
        .order_by('begin')
