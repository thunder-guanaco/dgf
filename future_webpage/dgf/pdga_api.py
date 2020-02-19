import requests
from urllib.parse import urlencode

base_url = 'https://api.pdga.com/services/json'


def logout(credentials):
    requests.post('{}/user/logout'.format(base_url), headers={'Content-type': 'application/json',
                                                              'Cookie': '{}={}'.format(
                                                                  credentials['session_name'],
                                                                  credentials['sessid']),
                                                              'X-CSRF-Token: ': credentials['token']})


def get_auth_token(credentials):
    return credentials['token']


def get_credentials(username, password):
    body = {'username': username, 'password': password}

    response = requests.post('{}/user/login'.format(base_url), json=body)
    return response


def query_player(credentials, first_name, last_name, pdga_number, player_class, city, state_prov, country,
                 last_modified, offset=0, limit=10):
    query = '?' + urlencode({
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
    })

    requests.get('{}/players{}'.format(base_url, query),
                 headers={'Cookie': '{}={}'.format(credentials['session_name'], credentials['sessid'])})


def query_player_statistics(credentials, year, player_class, gender, division_name, division_code, country, state_prov,
                            pdga_number, last_modified, offset=0, limit=10):
    query = '?' + urlencode({
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
    })

    requests.get('{}/player-statistics{}'.format(base_url, query),
                 headers={'Cookie': '{}={}'.format(credentials['session_name'], credentials['sessid'])})


def query_event(credentials, tournament_id, event_name, start_date, end_date, country, state, province,
                tier, classification, offset=0, limit=10):
    query = '?' + urlencode({
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
    })

    requests.get('{}/event{}'.format(base_url, query),
                 headers={'Cookie': '{}={}'.format(credentials['session_name'], credentials['sessid'])})
