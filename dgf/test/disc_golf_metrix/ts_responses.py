import json

import responses

from dgf.disc_golf_metrix import tremonia_series
from dgf_cms.settings import DISC_GOLF_METRIX_COMPETITION_ENDPOINT


def add_three_ts_tournaments():
    responses.add(responses.GET, DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(tremonia_series.ROOT_ID),
                  body=json.dumps(
                      {
                          'Competition': {
                              'Name': 'Tremonia Series',
                              'ID': tremonia_series.ROOT_ID,
                              'Events': [
                                  {
                                      'ID': '1',
                                      'Name': 'Tremonia Series #1 (Putter)'  # past tournament
                                  },
                                  {
                                      'ID': '22',
                                      'Name': '[DELETED] Tremonia Series #2'  # canceled
                                  },
                                  {
                                      'ID': '2',
                                      'Name': 'Tremonia Series #2 (Midrange)'  # second tournament again
                                  },
                                  {
                                      'ID': '3',
                                      'Name': 'Tremonia Series #3'  # future tournament
                                  }
                              ]
                          }
                      }),
                  status=200)

    add_ts_tournament(1, 'Tremonia Series #1 (Putter)', '1000-01-01')
    add_ts_tournament(2, 'Tremonia Series #2 (Midrange)', '2000-01-01')
    add_ts_tournament(3, 'Tremonia Series #3', '3000-01-01')


def add_five_ts_tournaments_for_tours(players):
    responses.add(responses.GET, DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(tremonia_series.ROOT_ID),
                  body=json.dumps(
                      {
                          'Competition': {
                              'Name': 'Tremonia Series',
                              'ID': tremonia_series.ROOT_ID,
                              'Events': [
                                  {
                                      'ID': '1',
                                      'Name': 'Tremonia Series #1'
                                  },
                                  {
                                      'ID': '2',
                                      'Name': 'Tremonia Series #2'
                                  },
                                  {
                                      'ID': '3',
                                      'Name': 'Tremonia Series #3'
                                  },
                                  {
                                      'ID': '4',
                                      'Name': 'Tremonia Series #4'
                                  },
                                  {
                                      'ID': '5',
                                      'Name': 'Tremonia Series #5'
                                  }
                              ]
                          }
                      }),
                  status=200)

    add_ts_tournament(1, 'Tremonia Series #1', '1000-01-01', players)
    add_ts_tournament(2, 'Tremonia Series #2', '1000-02-02', players)
    add_ts_tournament(3, 'Tremonia Series #3', '1000-03-03', players)
    add_ts_tournament(4, 'Tremonia Series #4', '2000-01-01', players)
    add_ts_tournament(5, 'Tremonia Series #5', '2000-02-02')


def add_one_ts_tournament(id, name, date_as_str, players=None, other_format=False):
    responses.add(responses.GET, DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(tremonia_series.ROOT_ID),
                  body=json.dumps(
                      {
                          'Competition': {
                              'Name': 'Tremonia Series',
                              'ID': tremonia_series.ROOT_ID,
                              'Events': [
                                  {
                                      'ID': f'{id}',
                                      'Name': name
                                  },
                              ]
                          }
                      }),
                  status=200)

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
