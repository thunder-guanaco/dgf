import responses
from django.conf import settings
from django.test import TestCase

from dgf.models import Friend
from dgf.pdga import PdgaApi


class PdgaApiTest(TestCase):

    @responses.activate
    def setUp(self):
        self.add_login()
        self.pdga_api = PdgaApi()

    @responses.activate
    def test_friend_has_no_pdga_number(self):
        fede = Friend.objects.create(username='fede', pdga_number=None, rating=None)

        self.pdga_api.update_friend_rating(fede)

        fede = Friend.objects.get(username='fede')
        self.assertIsNone(fede.rating)

    @responses.activate
    def test_rating_is_stored_in_friend(self):
        fede = Friend.objects.create(username='fede', pdga_number=109371, rating=None)
        self.set_responses_data(pdga_number=109371, rating=903)

        self.pdga_api.update_friend_rating(fede)

        fede = Friend.objects.get(username='fede')
        self.assertEqual(fede.rating, 903)

    @responses.activate
    def test_rating_is_updated_in_friend(self):
        fede = Friend.objects.create(username='fede', pdga_number=109371, rating=903)
        self.set_responses_data(pdga_number=109371, rating=947)

        self.pdga_api.update_friend_rating(fede)

        fede = Friend.objects.get(username='fede')
        self.assertEqual(fede.rating, 947)

    def set_responses_data(self, pdga_number=None, rating=None):

        if not pdga_number:
            raise TypeError('pdga_number should be set')
        if not rating:
            raise TypeError('rating should be set')

        responses.add(responses.GET,
                      f'{settings.PDGA_BASE_URL}/players?pdga_number={pdga_number}&offset=0&limit=10',
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
                                  'rating': f'{rating}',
                                  'rating_effective_date': '2020-03-10',
                                  'official_status': 'yes',
                                  'official_expiration_date': '2021-11-28',
                                  'last_modified': '2020-03-11'}]},
                      status=200)

    def add_login(self):
        responses.add(responses.POST, f'{settings.PDGA_BASE_URL}/user/login',
                      json={'session_name': 'SSESSf1f85588bb869a1781d21eec9fef1bff',
                            'sessid': 'pR2J-dQygl7B8fufkt4YPu-E-KOTeNJsvYyKFLaXXi8',
                            'token': 'uemWB6CbC0qwseuSJ7wogG65FsC7JNBsEXVOnR-xzQc'},
                      status=200)
