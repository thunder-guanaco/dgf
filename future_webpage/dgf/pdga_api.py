import requests

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
    query = '?'
    if first_name:
        query += 'first_name={}&'.format(first_name)

    if last_name:
        query += 'last_name={}&'.format(last_name)

    if pdga_number:
        query += 'pdga_number={}&'.format(pdga_number)

    if player_class:
        query += 'class={}&'.format(player_class)

    if city:
        query += 'city={}&'.format(city)

    if state_prov:
        query += 'state_prov={}&'.format(state_prov)

    if country:
        query += 'country={}&'.format(country)

    if last_modified:
        query += 'last_modified={}&'.format(last_modified)

    if offset:
        query += 'offset={}&'.format(offset)

    if limit:
        query += 'limit={}&'.format(limit)

    requests.get('{}/players{}'.format(base_url, query),
                 headers={'Cookie': '{}={}'.format(credentials['session_name'], credentials['sessid'])})


def query_player_statistics(credentials, year, player_class, gender, division_name, division_code, country, state_prov,
                            pdga_number, last_modified, offset=0, limit=10):
    query = '?'
    if year:
        query += 'year={}&'.format(year)

    if player_class:
        query += 'class={}&'.format(player_class)

    if gender:
        query += 'gender={}&'.format(gender)

    if division_name:
        query += 'division_name={}&'.format(division_name)

    if division_code:
        query += 'division_code={}&'.format(division_code)

    if state_prov:
        query += 'state_prov={}&'.format(state_prov)

    if country:
        query += 'country={}&'.format(country)

    if pdga_number:
        query += 'pdga_number={}&'.format(pdga_number)

    if last_modified:
        query += 'last_modified={}&'.format(last_modified)

    if offset:
        query += 'offset={}&'.format(offset)

    if limit:
        query += 'limit={}&'.format(limit)

    requests.get('{}/player-statistics{}'.format(base_url, query),
                 headers={'Cookie': '{}={}'.format(credentials['session_name'], credentials['sessid'])})


def query_event(credentials, tournament_id, event_name, start_date, end_date, country, state, province,
                tier, classification, offset=0, limit=10):
    query = '?'
    if tournament_id:
        query += 'tournament_id={}&'.format(tournament_id)

    if event_name:
        query += 'event_name={}&'.format(event_name)

    if start_date:
        query += 'start_date={}&'.format(start_date)

    if end_date:
        query += 'end_date={}&'.format(end_date)

    if country:
        query += 'country={}&'.format(country)

    if state:
        query += 'state={}&'.format(state)

    if province:
        query += 'province={}&'.format(province)

    if tier:
        query += 'tier={}&'.format(tier)

    if classification:
        query += 'classification={}&'.format(classification)

    if offset:
        query += 'offset={}&'.format(offset)

    if limit:
        query += 'limit={}&'.format(limit)

    requests.get('{}/event{}'.format(base_url, query),
                 headers={'Cookie': '{}={}'.format(credentials['session_name'], credentials['sessid'])})
