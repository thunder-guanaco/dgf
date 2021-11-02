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
            friend = Friend.all_objects.get(metrix_user_id=user_id)
            logger.info(f'Found Friend by Metrix User ID: {friend}')
            return friend

        except Friend.DoesNotExist:
            logger.info(f'Could not find Friend with Metrix User ID = "{user_id}"')
            return None


def find_friend_by_slugified_username(slugified_name):
    try:
        friend = Friend.all_objects.get(username=slugified_name)
        logger.info(f'Found Friend by slugified username: {friend}')
        return friend

    except Friend.DoesNotExist:
        logger.info(f'Could not find Friend with slugified username = "{slugified_name}"')
        return None


def find_friend_by_name(first_name, last_name):
    friends = Friend.all_objects.filter(first_name__icontains=first_name).filter(last_name__icontains=last_name)

    if friends.count() == 0:
        logger.info(f'Could not find Friend with first name = "{first_name}" and last name = "{last_name}"')
        return None

    if friends.count() == 1:
        friend = friends[0]
        logger.info(f'Found Friend by name: {friend}')
        return friend

    else:
        logger.info(f'Found more than one Friend with first name = "{first_name}" and last name = "{last_name}"')
        return None


def get_or_create_inactive_friend(user_id, slugified_name, first_name, last_name):
    """
    The Disc Golf Metrix user does not belong to the Disc Golf Friends.
    We do not want them to appear everywhere.
    Hence: is_active=False
    """

    friend = Friend.all_objects.create(username=slugified_name,
                                       slug=slugified_name,
                                       metrix_user_id=user_id,
                                       first_name=first_name,
                                       last_name=last_name,
                                       is_active=False
                                       )
    logger.info(f'Created Friend {friend}')
    return friend


def update_friend(friend, user_id, first_name, last_name):
    friend.metrix_user_id = user_id
    friend.first_name = first_name
    friend.last_name = last_name
    friend.save()


def find_friend(user_id, name):
    slugified_name = slugify(name)
    names = name.split(' ')
    first_name = names[0]
    last_name = ' '.join(names[1:])

    friend = find_friend_by_user_id(user_id)
    if friend is not None:
        return friend

    friend = find_friend_by_slugified_username(slugified_name)
    if friend is not None:
        update_friend(friend, user_id, first_name, last_name)
        return friend

    friend = find_friend_by_name(first_name, last_name)
    if friend is not None:
        update_friend(friend, user_id, first_name, last_name)
        return friend

    return get_or_create_inactive_friend(user_id, slugified_name, first_name, last_name)


def get_position(ts_result):
    try:
        return ts_result['Place']
    except KeyError:
        return ts_result['OrderNumber']


def add_attendance(tournament, ts_tournament):
    for ts_result in get_results(ts_tournament):
        friend = find_friend(ts_result['UserID'], ts_result['Name'])
        logger.info(f'Using Friend: {friend}')
        _, created = Attendance.objects.get_or_create(friend=friend, tournament=tournament)
        if created:
            logger.info(f'Added attendance of {friend} to {tournament}\n')


def add_results(tournament, ts_tournament):
    for ts_result in get_results(ts_tournament):
        friend = find_friend(ts_result['UserID'], ts_result['Name'])
        logger.info(f'Using Friend: {friend}')
        Result.objects.create(tournament=tournament,
                              friend=friend,
                              position=get_position(ts_result))
        logger.info(f'Added attendance of {friend} to {tournament}\n')


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
        logger.info(f'Created tournament {tournament}\n')
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

    # tournament is either not played yet or still in play
    if tournament.begin >= datetime.today():
        add_attendance(tournament, ts_tournament)

    # tournament was already played and does not have results
    elif tournament.results.count() == 0:
        add_results(tournament, ts_tournament)


def update_tournaments():
    tournament = get_tournament(TREMONIA_SERIES_ROOT_ID)
    for event in tournament['Events']:
        if not event['Name'].startswith('[DELETED]'):
            logger.info('--------------------------------------------------------------------------------\n')
            create_tournament(event['ID'])
