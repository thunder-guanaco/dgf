import json
import logging
from datetime import date, timedelta, datetime
from decimal import Decimal
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from dgf.models import Tournament, Attendance, Result, Division
from dgf_cms.settings import PDGA_DATE_FORMAT, PDGA_PAGE_BASE_URL

logger = logging.getLogger(__name__)


class PdgaApi:

    def __init__(self):
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

        For making requests to the PDGA you need to build a cookie that is a combination
        of the session_name and the sessid.
        """
        response = requests.post(f'{settings.PDGA_BASE_URL}/user/login',
                                 json={
                                     'username': settings.PDGA_USERNAME,
                                     'password': settings.PDGA_PASSWORD
                                 })

        if response.status_code != 200:
            raise ImproperlyConfigured('Credentials are not right. Please ensure that DJANGO_PDGA_USERNAME and '
                                       'DJANGO_PDGA_PASSWORD environment variables are correctly set')

        self.credentials = json.loads(response.content)

    def logout(self):
        requests.post(f'{settings.PDGA_BASE_URL}/user/logout', headers={'Content-type': 'application/json',
                                                                        'Cookie': f'{self.credentials["session_name"]}='
                                                                                  f'{self.credentials["sessid"]}',
                                                                        'X-CSRF-Token': self.credentials['token']})

    def query_player(self, first_name=None, last_name=None, pdga_number=None, player_class=None, city=None,
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

        return self._query_pdga('players', query_parameters)

    def query_player_statistics(self, year=None, player_class=None, gender=None, division_name=None,
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

        return self._query_pdga('player-statistics', query_parameters)

    def query_event(self, start_date=None, end_date=None, tournament_id=None, event_name=None, country=None,
                    state=None, province=None, tier=None, classification=None, offset=0, limit=10):
        """
        This method allows you to query events.
        It is crucial to add the start and the end date in the format 'YYYY-MM-DD'.
        This method is returning the complete content at the moment because on the testing time
        the PDGA was not returning anything more.
        """

        # just search for the next year's tournaments
        if start_date is None:
            start_date = date.today().strftime(PDGA_DATE_FORMAT)
        if end_date is None:
            end_date = (date.today() + timedelta(days=400)).strftime(PDGA_DATE_FORMAT)

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

        return self._query_pdga('event', query_parameters)

    def update_friend_rating(self, friend):
        if friend.pdga_number:
            pdga_friend_response = self.query_player(pdga_number=friend.pdga_number)
            rating = pdga_friend_response['players'][0]['rating']
            if rating:
                friend.rating = int(rating)
                friend.save()
                logger.info(f'{friend.username} has now rating: {friend.rating}')
            else:
                logger.info(
                    f'{friend.username} had no rating in the PDGA. Possible reasons: membership outdated or new member')

    def update_friend_tournament_statistics(self, friend):
        if friend.pdga_number:
            statistics = self.query_player_statistics(pdga_number=friend.pdga_number)

            money_earned = 0
            tournaments = 0

            try:
                players_statistics = statistics['players']
            except KeyError:
                logger.warning(f'{friend.username} has no statistics in their PDGA profile. '
                               f'Possible reasons: membership outdated or new member')

            for yearly_stats in players_statistics:
                try:
                    money_earned += Decimal(yearly_stats['prize'])
                except KeyError:
                    logger.warning(f'{friend.username} has no prices for a given year in their PDGA profile. '
                                   f'Possible reasons: player didn\'t win anything')
                try:
                    tournaments += int(yearly_stats['tournaments'])
                except KeyError:
                    logger.warning(f'{friend.username} has no tournaments for one given year in their PDGA profile. '
                                   f'Possible reasons: player didn\'t play any tournaments')

            friend.total_earnings = money_earned
            friend.total_tournaments = tournaments
            friend.save()

    def _query_pdga(self, url, query_parameters):
        query = urlencode({x: y for x, y in query_parameters.items() if y is not None})
        return json.loads(requests.get(f'{settings.PDGA_BASE_URL}/{url}?{query}',
                                       headers={
                                           'Cookie': f'{self.credentials["session_name"]}='
                                                     f'{self.credentials["sessid"]}'
                                       })
                          .content)


def get_page(url):
    url = f'{PDGA_PAGE_BASE_URL}{url}'
    logger.info(f'Getting {url}')
    return BeautifulSoup(requests.get(url).content, features='html5lib')


def get_player_page(pdga_number):
    return get_page(f'/player/{pdga_number}')


def extract_event_ids(events_li):
    events = events_li.find_all('a')
    return [event['href'].split('/')[-1] for event in events]


def get_upcoming_event_ids(player_page_soup):
    upcoming_events = player_page_soup.find('li', {'class': 'upcoming-events'})
    if upcoming_events:
        return extract_event_ids(upcoming_events)

    next_event = player_page_soup.find('li', {'class': 'next-event'})
    if next_event:
        return extract_event_ids(next_event)

    return []


def get_year_links(player_page_soup):
    year_links = player_page_soup.find('div', {'class': 'year-link'})
    if year_links:
        return [li.find('a').attrs['href'] for li in year_links.find_all('li')]
    else:
        return []


def add_tournament(pdga_api, pdga_id):
    event = pdga_api.query_event(tournament_id=pdga_id)
    pdga_tournament = event['events'][0]

    begin_date = datetime.strptime(pdga_tournament['start_date'], PDGA_DATE_FORMAT)
    end_date = datetime.strptime(pdga_tournament['end_date'], PDGA_DATE_FORMAT)

    tournament, created = Tournament.all_objects.get_or_create(pdga_id=pdga_tournament['tournament_id'],
                                                               defaults={
                                                                   'name': pdga_tournament['tournament_name'],
                                                                   'begin': begin_date,
                                                                   'end': end_date
                                                               })
    if created:
        logger.info(f'Created tournament {tournament}')
    else:
        # Always update. With Corona you never know
        tournament.name = pdga_tournament['tournament_name']
        tournament.begin = begin_date
        tournament.end = end_date
        tournament.save()

    return tournament


def add_attendance(friend, tournament):
    _, created = Attendance.objects.get_or_create(friend=friend, tournament=tournament)
    if created:
        logger.info(f'Added attendance of {friend} to {tournament}')


def add_result(friend, tournament, position, division):

    # get_or_create because we want to create legacy divisions
    division, created = Division.objects.get_or_create(id=division)
    if created:
        logger.info(f'Created division {division}')

    result, created = Result.objects.get_or_create(tournament=tournament,
                                                   friend=friend,
                                                   position=position,
                                                   defaults={'division': division})
    if created:
        logger.info(f'Added result: {result}')


def update_upcoming_events(pdga_api, friend, player_page_soup):
    event_ids = get_upcoming_event_ids(player_page_soup)
    for id in event_ids:
        tournament = add_tournament(pdga_api, pdga_id=id)
        add_attendance(friend, tournament)


def add_tournament_results(pdga_api, friend, year_link):
    year_page_soup = get_page(year_link)
    tables = year_page_soup.find_all('div', {'class': 'table-container'})
    for table in tables:
        trs = table.find('tbody').find_all('tr')
        for tr in trs:
            division = tr.find('td', {'class': 'tournament'}).find('a')['href'].split('#')[1]
            position = int(tr.find('td', {'class': 'place'}).text)
            tournament_url = tr.find('td', {'class': 'tournament'}).find('a').attrs['href']
            tournament_id = tournament_url.split('#')[0].split('/')[-1]
            tournament = add_tournament(pdga_api, pdga_id=tournament_id)
            add_result(friend, tournament, position, division)


def update_tournament_results(pdga_api, friend, player_page_soup):
    year_links = get_year_links(player_page_soup)
    for link in year_links:
        add_tournament_results(pdga_api, friend, link)


def update_friend_tournaments(friend, pdga_api):
    if friend.pdga_number:
        player_page_soup = get_player_page(friend.pdga_number)
        update_upcoming_events(pdga_api, friend, player_page_soup)
        update_tournament_results(pdga_api, friend, player_page_soup)
