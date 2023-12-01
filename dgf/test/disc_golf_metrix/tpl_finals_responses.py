import json

import responses

from dgf.disc_golf_metrix import tremonia_putting_liga_finals
from dgf.test.disc_golf_metrix.tpl_responses import tpl_player_results
from dgf_cms.settings import DISC_GOLF_METRIX_COMPETITION_ENDPOINT


def add_three_tpl_final_tournaments():
    responses.add(responses.GET, DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(tremonia_putting_liga_finals.ROOT_ID),
                  body=json.dumps(
                      {
                          'Competition': {
                              'Name': 'Tremonia Putting Liga &rarr; Finale-Runden',
                              'ID': tremonia_putting_liga_finals.ROOT_ID,
                              'HasSubcompetitions': 1,
                              'SubCompetitions': [
                                  {
                                      'ID': '1',
                                      'Name': 'Tremonia Putting Liga &rarr; Finale-Runden &rarr; 1. Spieltag'
                                      # past tournament
                                  },
                                  {
                                      'ID': '22',
                                      'Name': 'Tremonia Putting Liga &rarr; Finale-Runden &rarr; [DELETED] 2. Spieltag'
                                      # canceled
                                  },
                                  {
                                      'ID': '2',
                                      'Name': 'Tremonia Putting Liga &rarr; Finale-Runden &rarr; 2. Spieltag'
                                      # second tournament again
                                  },
                                  {
                                      'ID': '3',
                                      'Name': 'Tremonia Putting Liga &rarr; Finale-Runden &rarr; 3. Spieltag'
                                      # future tournament
                                  },
                              ]
                          }
                      }),
                  status=200)

    add_tpl_final_tournament(1, '1. Spieltag', '1000-01-01')
    add_tpl_final_tournament(2, '2. Spieltag', '2000-01-01')
    add_tpl_final_tournament(3, '3. Spieltag', '3000-01-01')


def add_three_tpl_finals_tournaments_for_tours(players):
    responses.add(responses.GET, DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(tremonia_putting_liga_finals.ROOT_ID),
                  body=json.dumps(
                      {
                          'Competition': {
                              'Name': 'Tremonia Putting Liga &rarr; Finale-Runden',
                              'ID': tremonia_putting_liga_finals.ROOT_ID,
                              'Events': [
                                  {
                                      'ID': '1',
                                      'Name': 'Tremonia Putting Liga &rarr; Finale-Runden &rarr; 1. Spieltag'
                                  },
                                  {
                                      'ID': '2',
                                      'Name': 'Tremonia Putting Liga &rarr; Finale-Runden &rarr; 2. Spieltag'
                                  },
                                  {
                                      'ID': '3',
                                      'Name': 'Tremonia Putting Liga &rarr; Finale-Runden &rarr; 3. Spieltag'
                                  },
                              ]
                          }
                      }),
                  status=200)

    add_tpl_final_tournament(1, '1. Spieltag', '1000-01-01', players)
    add_tpl_final_tournament(2, '2. Spieltag', '1000-02-02', players)
    add_tpl_final_tournament(3, '3. Spieltag', '1000-03-03')


def add_one_tpl_final_tournament(id, name, date_as_str, players=None):
    responses.add(responses.GET, DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(tremonia_putting_liga_finals.ROOT_ID),
                  body=json.dumps(
                      {
                          'Competition': {
                              'Name': 'Tremonia Putting Liga &rarr; Finale-Runden',
                              'ID': tremonia_putting_liga_finals.ROOT_ID,
                              'HasSubcompetitions': 1,
                              'SubCompetitions': [
                                  {
                                      'ID': f'{id}',
                                      'Name': f'Tremonia Putting Liga &rarr; Finale-Runden &rarr; {name}',
                                  },
                              ]
                          }
                      }),
                  status=200)

    add_tpl_final_tournament(id, name, date_as_str, players=players)


def add_tpl_final_tournament(id, name, date_as_str, players=None):
    if not players:
        players = []

    responses.add(responses.GET, DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(id),
                  body=json.dumps(
                      {
                          'Competition': {
                              'ID': id,
                              'Name': f'Tremonia Putting Liga &rarr; Finale-Runden &rarr; {name}',
                              'Date': date_as_str,
                              'HasSubcompetitions': 0,
                              'Results': [tpl_final_result(player) for player in players],
                          }
                      }),
                  status=200)


def tpl_final_result(player):
    return {
        'UserID': player[0],
        'Name': player[0],
        'Place': player[1],
        'ClassName': player[2],
        'PlayerResults': tpl_player_results(player[3])
    }
