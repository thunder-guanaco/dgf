from django.test import TestCase
import responses

from .models import Friend
from .pdga_fetcher import fill_friends_data
from django.conf import settings


class PdgaApiTest(TestCase):

    @responses.activate
    def test_rating_is_stored_in_friend(self):
        responses.add(responses.POST, '{}/user/login'.format(settings.PDGA_BASE_URL),
                      json='{"session_name": "SSESSf1f85588bb869a1781d21eec9fef1bff", '
                           '"sessid": "pR2J-dQygl7B8fufkt4YPu-E-KOTeNJsvYyKFLaXXi8”, '
                           '"token": "uemWB6CbC0qwseuSJ7wogG65FsC7JNBsEXVOnR-xzQc",}',
                      status=200)

        responses.add(responses.GET, '{}/players?pdga_number=109371'.format(settings.PDGA_BASE_URL),
                      json='{"sessid": "pR2J-dQygl7B8fufkt4YPu-E-KOTeNJsvYyKFLaXXi8", '
                           '"status": 0, "players": '
                           '[{"first_name": "Federico Jose", '
                           '"last_name": "Sorenson Sanchez", '
                           '"pdga_number": "109371", '
                           '"email_address": "fedejsoren@gmail.com", '
                           '"birth_year": "1988", '
                           '"gender": "M", '
                           '"membership_status": "current", '
                           '"membership_expiration_date": "2020-12-31", '
                           '"classification": "A", '
                           '"city": "M\u00e1laga", '
                           '"state_prov": "MA", '
                           '"country": "ES", '
                           '"rating": "903", '
                           '"rating_effective_date": "2020-03-10", '
                           '"official_status": "yes", '
                           '"official_expiration_date": "2021-11-28", '
                           '"last_modified": "2020-03-11"}]}',
                      status=200)
        print('calls')
        print(responses.calls)
        friend = Friend()
        friend.pdga_number = 109371

        fill_friends_data()

        all_friends = Friend.objects.all()
        print('friends')
        print(all_friends)
        a = 0
        #self.assertEqual(all_friends)

