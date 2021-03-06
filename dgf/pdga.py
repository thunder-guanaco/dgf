# coding=utf-8
import json
import logging
from decimal import Decimal
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

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
        response = requests.post('{}/user/login'.format(settings.PDGA_BASE_URL),
                                 json={
                                     'username': settings.PDGA_USERNAME,
                                     'password': settings.PDGA_PASSWORD
                                 })

        if response.status_code != 200:
            raise ImproperlyConfigured('Credentials are not right. Please ensure that DJANGO_PDGA_USERNAME and '
                                       'DJANGO_PDGA_PASSWORD environment variables are correctly set')

        self.credentials = json.loads(response.content)

    def logout(self):
        requests.post('{}/user/logout'.format(settings.PDGA_BASE_URL), headers={'Content-type': 'application/json',
                                                                                'Cookie': '{}={}'.format(
                                                                                    self.credentials['session_name'],
                                                                                    self.credentials['sessid']),
                                                                                'X-CSRF-Token: ': self.credentials[
                                                                                    'token']})

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

    def query_event(self, start_date, end_date, tournament_id=None, event_name=None, country=None,
                    state=None, province=None, tier=None, classification=None, offset=0, limit=10):
        """
        This method allows you to query events.
        It is crucial to add the start and the end date in the format 'YYYY-MM-DD'.
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

        return self._query_pdga('event', query_parameters)

    def update_friend_rating(self, friend):
        if friend.pdga_number:
            pdga_friend_response = self.query_player(pdga_number=friend.pdga_number)
            rating = pdga_friend_response['players'][0]['rating']
            if rating:
                friend.rating = int(rating)
                logger.info('{} has now rating: {}'.format(friend.username, friend.rating))
            else:
                logger.info(
                    '{} had no rating in the PDGA yet, possible reasons: membership outdated or new member'.format(
                        friend.username))

    def update_friend_tournament(self, friend):
        if friend.pdga_number:
            statistics = self.query_player_statistics(pdga_number=friend.pdga_number)

            money_earned = 0
            tournaments = 0
            for yearly_stats in statistics['players']:
                try:
                    money_earned += Decimal(yearly_stats['prize'])
                except KeyError:
                    # not all years have to have prizes
                    pass
                try:
                    tournaments += int(yearly_stats['tournaments'])
                except KeyError:
                    # maybe not all years have to have tournaments
                    pass

            friend.total_earnings = money_earned
            friend.total_tournaments = tournaments

    def _query_pdga(self, url, query_parameters):
        query = '?{}'.format(urlencode({x: y for x, y in query_parameters.items() if y is not None}))
        return json.loads(requests.get('{}/{}{}'.format(settings.PDGA_BASE_URL, url, query),
                                       headers={'Cookie': '{}={}'.format(self.credentials['session_name'],
                                                                         self.credentials['sessid'])}).content)
