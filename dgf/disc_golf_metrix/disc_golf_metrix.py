import logging
from datetime import datetime

import requests

from dgf import external_user_finder
from dgf.models import Tournament, Result, Attendance, Tour, Division
from dgf_cms.settings import DISC_GOLF_METRIX_COMPETITION_ENDPOINT, DISC_GOLF_METRIX_DATE_FORMAT

logger = logging.getLogger(__name__)


def get_tournament(id):
    url = DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(id)
    logger.info(f'GET {url}')
    return requests.get(url).json()['Competition']


def extract_name(dgm_tournament):
    return dgm_tournament['Name'].split(' &rarr; ')[-1]


def get_results(dgm_tournament):
    try:
        return dgm_tournament['TourResults']
    except KeyError:
        return dgm_tournament['SubCompetitions'][0]['Results']


def get_position(dgm_result):
    try:
        return dgm_result['Place']
    except KeyError:
        return dgm_result['OrderNumber']


def get_division(dgm_result, divisions):
    dgm_class = dgm_result.get('ClassName') or 'Open'
    return Division.objects.get(id=divisions[dgm_class])


def add_attendance(tournament, dgm_tournament):
    for dgm_result in get_results(dgm_tournament):
        friend = external_user_finder.find_friend(dgm_result['UserID'], dgm_result['Name'])
        logger.info(f'Using Friend: {friend}')
        _, created = Attendance.objects.get_or_create(friend=friend, tournament=tournament)
        if created:
            logger.info(f'Added attendance of {friend} to {tournament}\n')


def add_results(tournament, dgm_tournament, divisions):
    for dgm_result in get_results(dgm_tournament):
        friend = external_user_finder.find_friend(dgm_result['UserID'], dgm_result['Name'])
        logger.info(f'Using Friend: {friend}')
        result = Result.objects.create(tournament=tournament,
                                       friend=friend,
                                       position=get_position(dgm_result),
                                       division=get_division(dgm_result, divisions))
        logger.info(f'Added result: {result}')


def add_or_update_tournament(dgm_tournament, point_system):
    name = extract_name(dgm_tournament)
    date = datetime.strptime(dgm_tournament['Date'], DISC_GOLF_METRIX_DATE_FORMAT)
    dgm_id = dgm_tournament['ID']

    tournament, created = Tournament.objects.get_or_create(metrix_id=dgm_id,
                                                           defaults={
                                                               'name': name,
                                                               'begin': date,
                                                               'end': date,
                                                               'point_system': point_system,
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


def add_tours(tournament, tour_generator):
    divisions = tournament.results.filter(division__isnull=False).values_list('division', flat=True).distinct()

    if not divisions:
        logger.info(f'Skipping adding tours to {tournament.name} because it has no results (and no divisions)')
        return

    for name, evaluate_how_many in tour_generator(tournament):
        add_to_tour(name, tournament, divisions, evaluate_how_many)
        

def add_to_tour(name, tournament, divisions, evaluate_how_many=10000):
    for division in divisions:
        tour, created = Tour.objects.get_or_create(name=name,
                                                   division=Division.objects.get(id=division),
                                                   defaults={'evaluate_how_many': evaluate_how_many})

        if created:
            logger.info(f'Created Tour: {tour}')

        tournament.tours.add(tour)
        logger.info(f'Added {tournament} to {tour}')


def create_or_update_tournament(metrix_id, point_system, divisions, tour_generator):
    dgm_tournament = get_tournament(metrix_id)
    tournament = add_or_update_tournament(dgm_tournament, point_system)

    # tournament is either not played yet or still in play
    if tournament.begin >= datetime.today():
        add_attendance(tournament, dgm_tournament)

    # tournament was already played and does not have results
    elif tournament.results.count() == 0:
        add_results(tournament, dgm_tournament, divisions)
        tournament.recalculate_points()

    add_tours(tournament, tour_generator)


def update_tournaments(root_id, point_system, divisions, tour_generator):
    tournament = get_tournament(root_id)
    for event in tournament['Events']:
        if not event['Name'].startswith('[DELETED]'):
            logger.info('\n')
            create_or_update_tournament(event['ID'], point_system, divisions, tour_generator)
            logger.info('--------------------------------------------------------------------------------')
