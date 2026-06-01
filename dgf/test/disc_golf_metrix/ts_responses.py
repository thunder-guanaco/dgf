import json

import responses

from dgf_cms.settings import DISC_GOLF_METRIX_COMPETITION_ENDPOINT
from dgf_tremonia_series.models import MetrixIds


def add_three_ts_tournaments():
    MetrixIds.objects.create(ids='1,2,3')

    add_ts_tournament(1, 'Tremonia Series #1 (Putter)', '1000-01-01')
    add_ts_tournament(2, 'Tremonia Series #2 (Midrange)', '2000-01-01')
    add_ts_tournament(3, 'Tremonia Series #3', '3000-01-01')


def add_five_ts_tournaments_for_tours(players):
    MetrixIds.objects.create(ids='1,2,3,4,5')
    add_ts_tournament(1, 'Tremonia Series #1', '1000-01-01', players)
    add_ts_tournament(2, 'Tremonia Series #2', '1000-02-02', players)
    add_ts_tournament(3, 'Tremonia Series #3', '1000-03-03', players)
    add_ts_tournament(4, 'Tremonia Series #4', '2000-01-01', players)
    add_ts_tournament(5, 'Tremonia Series #5', '2000-02-02')


def add_one_ts_tournament(id, name, date_as_str, players=None, other_format=False):
    MetrixIds.objects.create(ids=f'{id}')

    if other_format:
        add_ts_tournament_with_other_format(id, name, date_as_str, players=players)
    else:
        add_ts_tournament(id, name, date_as_str, players=players)


def add_ts_tournament(id, name, date_as_str, players=None):
    if not players:
        players = []
    responses.add(responses.GET, DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(id),
                  body=json.dumps(
                      {
                          'Competition': {
                              'ID': id,
                              'Name': f'Tremonia Series &rarr; {name}',
                              'Date': date_as_str,
                              'TourResults': [ts_result(player, 'Place') for player in players]
                          }
                      }),
                  status=200)


def add_ts_tournament_with_other_format(id, name, date_as_str, players=None):
    if not players:
        players = []
    responses.add(responses.GET, DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(id),
                  body=json.dumps(
                      {
                          'Competition': {
                              'ID': id,
                              'Name': f'Tremonia Series &rarr; {name}',
                              'Date': date_as_str,
                              'SubCompetitions':
                                  [
                                      {
                                          'Results': [ts_result(player, 'OrderNumber') for player in
                                                      players]
                                      }
                                  ]
                          }
                      }),
                  status=200)


def ts_result(player, position_key):
    return {
        'UserID': player[0],
        'Name': player[0],
        position_key: player[1],
        'ClassName': player[2],
    }
