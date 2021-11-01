import logging
from datetime import datetime

import requests
from django.utils.text import slugify

from dgf.models import Tournament, Result, Friend, Attendance

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


def find_friend_by_user_id(user_id):
    if user_id is None:
        return None
    else:
        try:
            return Friend.objects.get(metrix_user_id=user_id)
        except Friend.DoesNotExist:
            return None


def find_friend_by_name(name, user_id):
    names = name.split(' ')
    # The Disc Golf Metrix user does not belong to the Disc Golf Friends.
    # We do not want them to appear everywhere.
    # Hence: active=False
    slugified_name = slugify(name)
    friend, created = Friend.all_objects.get_or_create(username=slugified_name,
                                                       defaults={
                                                           'slug': slugified_name,
                                                           'first_name': names[0],
                                                           'last_name': ' '.join(names[1:]),
                                                           'metrix_user_id': user_id,
                                                           'is_active': False
                                                       })
    if created:
        logger.info(f'Created friend {friend}')

    return friend


def find_friend(ts_result):
    user_id = ts_result['UserID']
    friend = find_friend_by_user_id(user_id)
    if friend is None:
        friend = find_friend_by_name(ts_result['Name'], ts_result['UserID'])
    return friend


def get_position(ts_result):
    try:
        return ts_result['Place']
    except KeyError:
        return ts_result['OrderNumber']


def add_results(tournament, ts_tournament):
    for ts_result in get_results(ts_tournament):
        friend = find_friend(ts_result)
        logger.info(f'Got friend: {friend}')
        _, created = Result.objects.get_or_create(tournament=tournament,
                                                  friend=friend,
                                                  position=get_position(ts_result))
        if created:
            logger.info(f'Added attendance of {friend} to {tournament}')


def add_attendance(tournament, ts_tournament):
    for ts_result in get_results(ts_tournament):
        friend = find_friend(ts_result)
        logger.info(f'Got friend: {friend}')
        _, created = Attendance.objects.get_or_create(friend=friend, tournament=tournament)
        if created:
            logger.info(f'Added attendance of {friend} to {tournament}')


def add_tournament(ts_tournament):
    name = extract_name(ts_tournament)
    date = datetime.strptime(ts_tournament['Date'], DISC_GOLF_METRIX_DATE_FORMAT)

    tournament, created = Tournament.objects.get_or_create(
        url=DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(ts_tournament['ID']),
        defaults={
            'name': name,
            'begin': date,
            'end': date,
        })

    if created:
        logger.info(f'Created tournament {tournament}')
    else:
        # Always update the name and the dates
        tournament.name = name
        tournament.begin = date
        tournament.end = date
        tournament.save()

    return tournament


def create_tournament(metrix_id):
    ts_tournament = get_tournament(metrix_id)
    tournament = add_tournament(ts_tournament)

    if tournament.date >= datetime.today():
        # tournament either not played yet or still in play
        add_attendance(tournament, ts_tournament)

    elif tournament.results.count() == 0:
        # tournament already played but without results
        add_results(tournament, ts_tournament)


def update_tournaments():
    tournament = get_tournament(TREMONIA_SERIES_ROOT_ID)
    for event in tournament['Events']:
        if not event['Name'].startswith('[DELETED]'):
            create_tournament(event['ID'])
