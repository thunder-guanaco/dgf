import logging
from datetime import datetime

import requests

from dgf.models import Tournament, Result, Friend

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


def find_friend(ts_tournament):
    try:
        return Friend.objects.get(metrix_user_id=ts_tournament['UserID'])
    except Friend.DoesNotExist:
        try:
            return Friend.objects.get(first_name__icontains=ts_tournament['Name'])
        except Friend.DoesNotExist:
            first_name, last_name = ts_tournament['Name'].split(' ')
            # The Disc Golf Metrix user does not belong to the Disc Golf Friends.
            # We do not want them to appear everywhere.
            # Hence: active=False
            Friend.objects.create(first_name=first_name,
                                  last_name=last_name,
                                  metrix_user_id=ts_tournament['UserID'],
                                  is_active=False)

    def add_results(tournament, ts_tournament):
        import ipdb
        ipdb.set_trace()
        for ts_tournament in ts_tournament['TourResults']:
            Result.objects.create(tournament=tournament,
                                  friend=find_friend(ts_tournament),
                                  position=ts_tournament['Place'])

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

        add_results(tournament, ts_tournament)

def create_tournament(id):
    tournament = get_tournament(id)
    add_tournament(tournament)

def update_tournaments():
    tournament = get_tournament(TREMONIA_SERIES_ROOT_ID)
    for event in tournament['Events']:
        if not event['Name'].startswith('[DELETED]'):
            create_tournament(event['ID'])
