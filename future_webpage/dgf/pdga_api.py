# coding=utf-8
import requests
import json
from urllib import urlencode

base_url = 'https://api.pdga.com/services/json'


def logout(credentials):
    requests.post('{}/user/logout'.format(base_url), headers={'Content-type': 'application/json',
                                                              'Cookie': '{}={}'.format(
                                                                  credentials['session_name'],
                                                                  credentials['sessid']),
                                                              'X-CSRF-Token: ': credentials['token']})


def get_credentials(username, password):
    """
    This method returns the credentials provided from the PDGA.
    This credentials have the following format:
    {
        "session_name": "SSESSf1f85588bb869a1781d21eec9fef1bff",
        "sessid": "pR2J-dQygl7B8fufkt4YPu-E-KOTeNJsvYyKFLaXXi8”,
        "token": "uemWB6CbC0qwseuSJ7wogG65FsC7JNBsEXVOnR-xzQc",
        "user": {
        ...
        }
    }

    For making requests to the PDGA you need to build a cookie that is a combination of the session_name and the sessid.
    """
    body = {'username': username, 'password': password}

    response = requests.post('{}/user/login'.format(base_url), json=body)
    return json.loads(response.content)


def query_pdga(credentials, url, query_parameters):
    query = '?{}'.format(urlencode({x: y for x, y in query_parameters.items() if y is not None}))
    return json.loads(requests.get('{}/{}{}'.format(base_url, url, query),
                                   headers={'Cookie': '{}={}'.format(credentials['session_name'],
                                                                     credentials['sessid'])}).content)


def query_player(credentials, first_name=None, last_name=None, pdga_number=None, player_class=None, city=None,
                 state_prov=None, country=None, last_modified=None, offset=0, limit=10):
    """
    This method allows you to fetch the basic information (personal data) of the queried players.
    """

    query_parameters = {
        'first_name': first_name,
        'last_name': last_name,
        'pdga_number': pdga_number,
        'class': player_class,
        'city': city,
        'state_prov': state_prov,
        'country': country,
        'last_modified': last_modified,
        'offset': offset,
        'limit': limit
    }

    return query_pdga(credentials, 'players', query_parameters)


def query_player_statistics(credentials, year=None, player_class=None, gender=None, division_name=None,
                            division_code=None, country=None, state_prov=None, pdga_number=None, last_modified=None,
                            offset=0, limit=10):
    """
    This method allows you to query the statistics of a player. This method is returning the complete content at the
    moment because on the testing time the PDGA was not returning anything more.
    """

    query_parameters = {
        'year': year,
        'class': player_class,
        'gender': gender,
        'division_name': division_name,
        'division_code': division_code,
        'country': country,
        'state_prov': state_prov,
        'pdga_number': pdga_number,
        'last_modified': last_modified,
        'offset': offset,
        'limit': limit
    }

    return query_pdga(credentials, 'player-statistics', query_parameters)


def query_event(credentials, start_date, end_date, tournament_id=None, event_name=None, country=None,
                state=None, province=None, tier=None, classification=None, offset=0, limit=10):
    """
    This method allows you to query events. It is crucial to add the start and the end date in the format 'YYYY-MM-DD'.
    This method is returning the complete content at the moment because on the testing time
    the PDGA was not returning anything more.
    """
    query_parameters = {
        'tournament_id': tournament_id,
        'event_name': event_name,
        'start_date': start_date,
        'end_date': end_date,
        'country': country,
        'state': state,
        'province': province,
        'tier': tier,
        'classification': classification,
        'offset': offset,
        'limit': limit
    }

    return query_pdga(credentials, 'event', query_parameters)
