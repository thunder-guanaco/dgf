from decimal import Decimal

import responses
from django.conf import settings
from django.test import TestCase

from ...cronjobs import fetch_pdga_data
from ...models import Friend


class PdgaApiTest(TestCase):

    @responses.activate
    def test_rating_is_stored_in_friend(self):
        self.configure_responses()

        friend = Friend()
        friend.pdga_number = 109371
        friend.username = 'fede'
        friend.save()
        fetch_pdga_data()
        self.assertEqual(Friend.objects.get(pdga_number='109371').rating, 903)

    @responses.activate
    def test_rating_is_stored_in_friend_when_saved(self):
        self.configure_responses()

        friend = Friend()
        friend.pdga_number = 109371
        friend.username = 'fede'
        friend.save()
        self.assertEqual(Friend.objects.get(pdga_number='109371').rating, 903)

    @responses.activate
    def test_prices_and_tournaments_stored(self):
        self.configure_responses()

        friend = Friend()
        friend.pdga_number = 47163
        friend.username = 'kevin'
        friend.save()
        fetch_pdga_data()
        kevin = Friend.objects.get(pdga_number='47163')
        self.assertEqual(kevin.total_tournaments, 97)
        self.assertEqual(kevin.total_earnings, Decimal('3981.05'))

    def configure_responses(self):
        self.add_login()
        self.add_friend_data('47163')
        self.add_friend_data('109371')
        self.add_friend_statistics('47163')
        self.add_friend_statistics('109371')

    def add_friend_data(self, pdga_number):
        responses.add(responses.GET,
                      '{}/players?pdga_number={}&offset=0&limit=10'.format(settings.PDGA_BASE_URL, pdga_number),
                      json={'sessid': 'pR2J-dQygl7B8fufkt4YPu-E-KOTeNJsvYyKFLaXXi8',
                            'status': 0, 'players':
                                [{'first_name': 'Federico Jose',
                                  'last_name': 'Sorenson Sanchez',
                                  'pdga_number': '109371',
                                  'email_address': 'fedejsoren@gmail.com',
                                  'birth_year': '1988',
                                  'gender': 'M',
                                  'membership_status': 'current',
                                  'membership_expiration_date': '2020-12-31',
                                  'classification': 'A', 'city': 'M\u00e1laga',
                                  'state_prov': 'MA',
                                  'country': 'ES',
                                  'rating': '903',
                                  'rating_effective_date': '2020-03-10',
                                  'official_status': 'yes',
                                  'official_expiration_date': '2021-11-28',
                                  'last_modified': '2020-03-11'}]},
                      status=200)

    def add_login(self):
        responses.add(responses.POST, '{}/user/login'.format(settings.PDGA_BASE_URL),
                      json={'session_name': 'SSESSf1f85588bb869a1781d21eec9fef1bff',
                            'sessid': 'pR2J-dQygl7B8fufkt4YPu-E-KOTeNJsvYyKFLaXXi8',
                            'token': 'uemWB6CbC0qwseuSJ7wogG65FsC7JNBsEXVOnR-xzQc'},
                      status=200)

    def add_friend_statistics(self, pdga_number):
        responses.add(responses.GET,
                      '{}/player-statistics?pdga_number={}&offset=0&limit=10'.format(settings.PDGA_BASE_URL,
                                                                                     pdga_number),
                      json={'sessid': 'M5EGJLLqYVKIl1b5hczcWrEXfUPYtYWZEz5Fs6JU1oQ',
                            'status': 0,
                            'players': [{'first_name': 'Kevin',
                                         'last_name': 'Konsorr',
                                         'pdga_number': '47163',
                                         'rating': '1007',
                                         'year': '2019',
                                         'class': 'P',
                                         'gender': 'Male',
                                         'division_name': 'Open',
                                         'division_code': 'MPO',
                                         'country': 'Germany',
                                         'tournaments': '14',
                                         'rating_rounds_used': '33',
                                         'points': '3737',
                                         'prize': '747.98',
                                         'last_modified': '2019-11-13'},
                                        {'first_name': 'Kevin',
                                         'last_name': 'Konsorr',
                                         'pdga_number': '47163',
                                         'rating': '987',
                                         'year': '2013',
                                         'class': 'P',
                                         'gender': 'Male',
                                         'division_name': 'Open',
                                         'division_code': 'MPO',
                                         'country': 'Germany',
                                         'tournaments': '15',
                                         'rating_rounds_used': '33',
                                         'points': '3437',
                                         'prize': '179.82',
                                         'last_modified': '2018-05-15'},
                                        {'first_name': 'Kevin',
                                         'last_name': 'Konsorr',
                                         'pdga_number': '47163',
                                         'rating': '996',
                                         'year': '2014',
                                         'class': 'P',
                                         'gender': 'Male',
                                         'division_name': 'Open',
                                         'division_code': 'MPO',
                                         'country': 'Germany',
                                         'tournaments': '10',
                                         'rating_rounds_used': '33',
                                         'points': '2425',
                                         'prize': '903.28',
                                         'last_modified': '2018-02-27'},
                                        {'first_name': 'Kevin',
                                         'last_name': 'Konsorr',
                                         'pdga_number': '47163',
                                         'rating': '1010',
                                         'year': '2018',
                                         'class': 'P',
                                         'gender': 'Male',
                                         'division_name': 'Open',
                                         'division_code': 'MPO',
                                         'country': 'Germany',
                                         'tournaments': '11',
                                         'rating_rounds_used': '33',
                                         'points': '2320',
                                         'prize': '1351.57',
                                         'last_modified': '2019-11-01'},
                                        {'first_name': 'Kevin',
                                         'last_name': 'Konsorr',
                                         'pdga_number': '47163',
                                         'rating': '1004',
                                         'year': '2017',
                                         'class': 'P',
                                         'gender': 'Male',
                                         'division_name': 'Open',
                                         'division_code': 'MPO',
                                         'country': 'Germany',
                                         'tournaments': '12',
                                         'rating_rounds_used': '33',
                                         'points': '2112',
                                         'prize': '151.21',
                                         'last_modified': '2018-02-28'},
                                        {'first_name': 'Kevin',
                                         'last_name': 'Konsorr',
                                         'pdga_number': '47163',
                                         'rating': '1007',
                                         'year': '2016',
                                         'class': 'P',
                                         'gender': 'Male',
                                         'division_name': 'Open',
                                         'division_code': 'MPO',
                                         'country': 'Germany',
                                         'tournaments': '8',
                                         'rating_rounds_used': '33',
                                         'points': '1412',
                                         'prize': '557.95',
                                         'last_modified': '2018-02-27'},
                                        {'first_name': 'Kevin',
                                         'last_name': 'Konsorr',
                                         'pdga_number': '47163',
                                         'rating': '990',
                                         'year': '2015',
                                         'class': 'P',
                                         'gender': 'Male',
                                         'division_name': 'Open',
                                         'division_code': 'MPO',
                                         'country': 'Germany',
                                         'tournaments': '5',
                                         'rating_rounds_used': '33',
                                         'points': '850',
                                         'prize': '89.24',
                                         'last_modified': '2018-02-27'},
                                        {'first_name': 'Kevin',
                                         'last_name': 'Konsorr',
                                         'pdga_number': '47163',
                                         'rating': '987',
                                         'year': '2012',
                                         'class': 'P',
                                         'gender': 'Male',
                                         'division_name': 'Junior I Boys',
                                         'division_code': 'MJ1',
                                         'country': 'Germany',
                                         'tournaments': '13',
                                         'rating_rounds_used': '33',
                                         'points': '272',
                                         'prize': '0',
                                         'last_modified': '2018-02-14'},
                                        {'first_name': 'Kevin',
                                         'last_name': 'Konsorr',
                                         'pdga_number': '47163',
                                         'rating': '987',
                                         'year': '2012',
                                         'class': 'P',
                                         'gender': 'Male',
                                         'division_name': 'Open',
                                         'division_code': 'MPO',
                                         'country': 'Germany',
                                         'tournaments': '1',
                                         'rating_rounds_used': '33',
                                         'points': '220',
                                         'prize': '0',
                                         'last_modified': '2018-02-14'},
                                        {'first_name': 'Kevin',
                                         'last_name': 'Konsorr',
                                         'pdga_number': '47163',
                                         'rating': '979',
                                         'year': '2011',
                                         'class': 'P',
                                         'gender': 'Male',
                                         'division_name': 'Open',
                                         'division_code': 'MPO',
                                         'country': 'Germany',
                                         'tournaments': '1',
                                         'rating_rounds_used': '33',
                                         'points': '200',
                                         'prize': '0',
                                         'last_modified': '2018-02-14'},
                                        {'first_name': 'Kevin',
                                         'last_name': 'Konsorr',
                                         'pdga_number': '47163',
                                         'rating': '1007',
                                         'year': '2020',
                                         'class': 'P',
                                         'gender': 'Male',
                                         'division_name': 'Open',
                                         'division_code': 'MPO',
                                         'country': 'Germany',
                                         'tournaments': '1',
                                         'rating_rounds_used': '33',
                                         'points': '60',
                                         'last_modified': '2020-02-24'},
                                        {'first_name': 'Kevin',
                                         'last_name': 'Konsorr',
                                         'pdga_number': '47163',
                                         'rating': '979',
                                         'year': '2011',
                                         'class': 'P',
                                         'gender': 'Male',
                                         'division_name': 'Junior I Boys',
                                         'division_code': 'MJ1',
                                         'country': 'Germany',
                                         'tournaments': '4',
                                         'rating_rounds_used': '33',
                                         'points': '50',
                                         'prize': '0',
                                         'last_modified': '2018-02-14'},
                                        {'first_name': 'Kevin',
                                         'last_name': 'Konsorr',
                                         'pdga_number': '47163',
                                         'rating': '987',
                                         'year': '2012',
                                         'class': 'P',
                                         'gender': 'Male',
                                         'division_name': 'Junior II Boys',
                                         'division_code': 'MJ2',
                                         'country': 'Germany',
                                         'tournaments': '2',
                                         'rating_rounds_used': '33',
                                         'points': '25',
                                         'prize': '0',
                                         'last_modified': '2018-02-14'}]},
                      status=200)
