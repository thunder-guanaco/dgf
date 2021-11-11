from datetime import date, timedelta

import responses
from django.conf import settings
from django.test import TestCase

from dgf import pdga
from dgf.models import Friend, Attendance, Tournament
from dgf.pdga import PDGA_DATE_FORMAT, PdgaApi

APRIL_2 = date(year=2021, month=4, day=2)
JULY_24 = date(year=2021, month=7, day=24)
JULY_25 = date(year=2021, month=7, day=25)


class PdgaTournamentAttendanceTest(TestCase):

    @responses.activate
    def setUp(self):
        self.add_login()
        self.pdga_api = PdgaApi()
        Friend.objects.all().delete()
        Tournament.objects.all().delete()
        Attendance.objects.all().delete()

    def test_no_pdga_number_no_attendance(self):
        manolo = Friend.objects.create(username='manolo')

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        attendance_list = list(Attendance.objects.filter(friend=manolo))
        self.assertListEqual(attendance_list, [])

    def test_no_pdga_number_but_attendance(self):
        manolo = Friend.objects.create(username='manolo')
        tournament = Tournament.objects.create(pdga_id=123, name='test', begin=date.today(), end=date.today())
        existing_attendance = Attendance.objects.create(friend=manolo, tournament=tournament)

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        attendance_list = list(Attendance.objects.filter(friend=manolo))
        self.assertListEqual(attendance_list, [existing_attendance])

    @responses.activate
    def test_without_events_no_attendance(self):
        self.fake_pdga_player_page_without_events(111828)

        manolo = Friend.objects.create(username='manolo', pdga_number=111828)

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        attendance_list = list(Attendance.objects.filter(friend=manolo))
        self.assertListEqual(attendance_list, [])

    @responses.activate
    def test_without_events_but_attendance(self):
        self.fake_pdga_player_page_without_events(111828)

        manolo = Friend.objects.create(username='manolo', pdga_number=111828)
        ts3 = Tournament.objects.create(pdga_id=333, name='Tremonia Series #3', begin=JULY_24, end=JULY_24)
        Attendance.objects.create(friend=manolo, tournament=ts3)

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        attendance_list = Attendance.objects.filter(friend=manolo)
        self.assertEqual(len(attendance_list), 1)

        attendance_ts3 = attendance_list.get(tournament__pdga_id=333)
        self.assertEqual(attendance_ts3.tournament, ts3)
        self.assertEqual(attendance_ts3.friend, manolo)

    @responses.activate
    def test_next_event_no_attendance_no_tournament(self):
        self.add_tournament_data('333', 'Tremonia Series #3', '2021-07-24', '2021-07-24')
        self.fake_pdga_player_page_with_next_event(111828)

        manolo = Friend.objects.create(username='manolo', pdga_number=111828)

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        attendance_list = Attendance.objects.filter(friend=manolo)
        self.assertEqual(len(attendance_list), 1)

        attendance_ts3 = attendance_list.get(tournament__pdga_id=333)
        self.assertEqual(attendance_ts3.tournament.name, 'Tremonia Series #3')
        self.assertEqual(attendance_ts3.tournament.url, 'https://www.pdga.com/tour/event/333')
        self.assertEqual(attendance_ts3.tournament.begin, JULY_24)
        self.assertEqual(attendance_ts3.tournament.end, JULY_24)
        self.assertEqual(attendance_ts3.friend, manolo)

    @responses.activate
    def test_next_event_no_attendance_existing_tournament(self):
        self.add_tournament_data('333', 'Tremonia Series #3', '2021-07-24', '2021-07-24')
        self.fake_pdga_player_page_with_next_event(111828)

        manolo = Friend.objects.create(username='manolo', pdga_number=111828)
        ts3 = Tournament.objects.create(pdga_id=333, name='Tremonia Series #3', begin=JULY_24, end=JULY_24)

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        attendance_list = Attendance.objects.filter(friend=manolo)
        self.assertEqual(len(attendance_list), 1)

        attendance_ts3 = attendance_list.get(tournament__pdga_id=333)
        self.assertEqual(attendance_ts3.tournament, ts3)
        self.assertEqual(attendance_ts3.friend, manolo)

    @responses.activate
    def test_next_event_existing_attendance_existing_tournament(self):
        self.add_tournament_data('333', 'Tremonia Series #3', '2021-07-24', '2021-07-24')
        self.fake_pdga_player_page_with_next_event(111828)

        manolo = Friend.objects.create(username='manolo', pdga_number=111828)
        ts3 = Tournament.objects.create(pdga_id=333, name='Tremonia Series #3', begin=JULY_24, end=JULY_24)
        Attendance.objects.create(friend=manolo, tournament=ts3)

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        attendance_list = Attendance.objects.filter(friend=manolo)
        self.assertEqual(len(attendance_list), 1)

        attendance_ts3 = attendance_list.get(tournament__pdga_id=333)
        self.assertEqual(attendance_ts3.tournament.name, 'Tremonia Series #3')
        self.assertEqual(attendance_ts3.tournament.url, 'https://www.pdga.com/tour/event/333')
        self.assertEqual(attendance_ts3.tournament.begin, JULY_24)
        self.assertEqual(attendance_ts3.tournament.end, JULY_24)
        self.assertEqual(attendance_ts3.friend, manolo)

    @responses.activate
    def test_upcoming_events_no_attendance_no_tournaments(self):
        self.add_tournament_data('333', 'Tremonia Series #3', '2021-07-24', '2021-07-24')
        self.add_tournament_data('444', 'Tremonia Series #4', '2021-07-24', '2021-07-25')
        self.fake_pdga_player_page_with_upcoming_events(111828)

        manolo = Friend.objects.create(username='manolo', pdga_number=111828)

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        attendance_list = Attendance.objects.filter(friend=manolo)
        self.assertEqual(len(attendance_list), 2)

        attendance_ts3 = attendance_list.get(tournament__pdga_id=333)
        self.assertEqual(attendance_ts3.tournament.name, 'Tremonia Series #3')
        self.assertEqual(attendance_ts3.tournament.url, 'https://www.pdga.com/tour/event/333')
        self.assertEqual(attendance_ts3.tournament.begin, JULY_24)
        self.assertEqual(attendance_ts3.tournament.end, JULY_24)
        self.assertEqual(attendance_ts3.friend, manolo)

        attendance_ts4 = attendance_list.get(tournament__pdga_id=444)
        self.assertEqual(attendance_ts4.tournament.name, 'Tremonia Series #4')
        self.assertEqual(attendance_ts4.tournament.url, 'https://www.pdga.com/tour/event/444')
        self.assertEqual(attendance_ts4.tournament.begin, JULY_24)
        self.assertEqual(attendance_ts4.tournament.end, JULY_25)
        self.assertEqual(attendance_ts4.friend, manolo)

    @responses.activate
    def test_upcoming_events_no_attendance_existing_tournaments(self):
        self.add_tournament_data('333', 'Tremonia Series #3', '2021-07-24', '2021-07-24')
        self.add_tournament_data('444', 'Tremonia Series #4', '2021-07-24', '2021-07-25')
        self.fake_pdga_player_page_with_upcoming_events(111828)

        manolo = Friend.objects.create(username='manolo', pdga_number=111828)
        ts3 = Tournament.objects.create(pdga_id=333, name='Tremonia Series #3', begin=JULY_24, end=JULY_24)
        ts4 = Tournament.objects.create(pdga_id=444, name='Tremonia Series #4', begin=JULY_24, end=JULY_25)

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        attendance_list = Attendance.objects.filter(friend=manolo)
        self.assertEqual(len(attendance_list), 2)

        attendance_ts3 = attendance_list.get(tournament__pdga_id=333)
        self.assertEqual(attendance_ts3.tournament, ts3)
        self.assertEqual(attendance_ts3.friend, manolo)

        attendance_ts4 = attendance_list.get(tournament__pdga_id=444)
        self.assertEqual(attendance_ts4.tournament, ts4)
        self.assertEqual(attendance_ts4.friend, manolo)

    @responses.activate
    def test_upcoming_events_existing_attendance_existing_tournaments(self):
        self.add_tournament_data('333', 'Tremonia Series #3', '2021-07-24', '2021-07-24')
        self.add_tournament_data('444', 'Tremonia Series #4', '2021-07-24', '2021-07-25')
        self.fake_pdga_player_page_with_upcoming_events(111828)

        manolo = Friend.objects.create(username='manolo', pdga_number=111828)
        ts3 = Tournament.objects.create(pdga_id=333, name='Tremonia Series #3', begin=JULY_24, end=JULY_24)
        ts4 = Tournament.objects.create(pdga_id=444, name='Tremonia Series #4', begin=JULY_24, end=JULY_25)
        Attendance.objects.create(friend=manolo, tournament=ts3)
        Attendance.objects.create(friend=manolo, tournament=ts4)

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        attendance_list = Attendance.objects.filter(friend=manolo)
        self.assertEqual(len(attendance_list), 2)

        attendance_ts3 = attendance_list.get(tournament__pdga_id=333)
        self.assertEqual(attendance_ts3.tournament, ts3)
        self.assertEqual(attendance_ts3.friend, manolo)

        attendance_ts4 = attendance_list.get(tournament__pdga_id=444)
        self.assertEqual(attendance_ts4.tournament, ts4)
        self.assertEqual(attendance_ts4.friend, manolo)

    @responses.activate
    def test_upcoming_events_name_change(self):
        self.add_tournament_data('333', 'Tremonia Series #3', '2021-07-24', '2021-07-24')
        self.add_tournament_data('444', 'Tremonia Series #4', '2021-07-24', '2021-07-25')
        self.fake_pdga_player_page_with_upcoming_events(111828)

        manolo = Friend.objects.create(username='manolo', pdga_number=111828)
        Tournament.objects.create(pdga_id=333, name='Tremonia Series #33', begin=JULY_24, end=JULY_24)
        Tournament.objects.create(pdga_id=444, name='Tremonia Series #43', begin=JULY_24, end=JULY_25)

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        ts3 = Tournament.objects.get(pdga_id=333)
        self.assertEqual(ts3.name, 'Tremonia Series #3')

        ts4 = Tournament.objects.get(pdga_id=444)
        self.assertEqual(ts4.name, 'Tremonia Series #4')

    @responses.activate
    def test_upcoming_events_date_change(self):
        self.add_tournament_data('333', 'Tremonia Series #3', '2021-07-24', '2021-07-24')
        self.add_tournament_data('444', 'Tremonia Series #4', '2021-07-24', '2021-07-25')
        self.fake_pdga_player_page_with_upcoming_events(111828)

        manolo = Friend.objects.create(username='manolo', pdga_number=111828)
        Tournament.objects.create(pdga_id=333, name='Tremonia Series #3', begin=APRIL_2, end=APRIL_2)
        Tournament.objects.create(pdga_id=444, name='Tremonia Series #4', begin=JULY_24, end=JULY_24)

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        ts3 = Tournament.objects.get(pdga_id=333)
        self.assertEqual(ts3.begin, JULY_24)
        self.assertEqual(ts3.end, JULY_24)

        ts4 = Tournament.objects.get(pdga_id=444)
        self.assertEqual(ts4.begin, JULY_24)
        self.assertEqual(ts4.end, JULY_25)

    def add_tournament_data(self, tournament_id, tournament_name, start_date, end_date):
        search_start_date = date.today()
        search_end_date = date.today() + timedelta(days=400)
        responses.add(responses.GET,
                      f'{settings.PDGA_BASE_URL}/event'
                      f'?tournament_id={tournament_id}'
                      f'&start_date={search_start_date.strftime(PDGA_DATE_FORMAT)}'
                      f'&end_date={search_end_date.strftime(PDGA_DATE_FORMAT)}'
                      f'&offset=0'
                      f'&limit=10',
                      json={'sessid': 'M5EGJLLqYVKIl1b5hczcWrEXfUPYtYWZEz5Fs6JU1oQ',
                            'status': 0,
                            'events': [
                                {
                                    'tournament_id': tournament_id,
                                    'tournament_name': tournament_name,
                                    'city': 'Dortmund',
                                    'state_prov': 'NRW',
                                    'country': 'Germany',
                                    'latitude': '51.519577',
                                    'longitude': '7.399750',
                                    'start_date': start_date,
                                    'end_date': end_date,
                                    'class': 'Am',
                                    'tier': 'C',
                                    'status': 'sanctioned',
                                    'format': 'singles',
                                    'tournament_director': 'Manuel García García',
                                    'tournament_director_pdga_number': '111828',
                                    'asst_tournament_director': 'Federico José Sörenson Sánchez',
                                    'asst_tournament_director_pdga_number': '109371',
                                    'event_email': 'mgg@example.com',
                                    'event_phone': '012-345-6789',
                                    'event_url': f'https://www.pdga.com/tour/event/{tournament_id}',
                                    'website_url': 'https://discgolffriends.de/turniere/tremonia-series',
                                    'registration_url': 'https://discgolfmetrix.com/715021',
                                    'last_modified': '2021-03-15'
                                }
                            ]},
                      status=200)

    def add_login(self):
        responses.add(responses.POST, f'{settings.PDGA_BASE_URL}/user/login',
                      json={'session_name': 'SSESSf1f85588bb869a1781d21eec9fef1bff',
                            'sessid': 'pR2J-dQygl7B8fufkt4YPu-E-KOTeNJsvYyKFLaXXi8',
                            'token': 'uemWB6CbC0qwseuSJ7wogG65FsC7JNBsEXVOnR-xzQc'},
                      status=200)

    def fake_pdga_player_page_without_events(self, pdga_number):
        responses.add(responses.GET, f'https://www.pdga.com/player/{pdga_number}',
                      body='<div class="pane-content">'
                           '  <ul class="player-info info-list">'
                           '    <li class="location">'
                           '      <strong>Location:</strong>'
                           '      <a href="/players?City=M%C3%A1laga&amp;Country=ES">Málaga, Málaga, Spain</a>'
                           '    </li>'
                           '    <li class="classification">'
                           '      <strong>Classification: </strong>'
                           '        Amateur'
                           '    </li>'
                           '    <li class="join-date">'
                           '      <strong>Member Since:</strong>'
                           '        2018'
                           '      </li>'
                           '    <li class="membership-status">'
                           '      <strong>Membership Status: </strong>'
                           '      <a href="/membership">Current</a>'
                           '      <small class="membership-expiration-date">(until 31-Dec-2021)</small>'
                           '    </li>'
                           '    <li class="current-rating">'
                           '      <strong>Current Rating:</strong> 895'
                           '      <small class="rating-date">(as of 11-Aug-2020)</small>'
                           '    </li>'
                           '    <li class="career-events disclaimer" title="Singles-format tournaments played.">'
                           '      <strong>Career Events:</strong>'
                           '      12'
                           '    </li>'
                           '  </ul>'
                           '</div>')

    def fake_pdga_player_page_with_next_event(self, pdga_number):
        responses.add(responses.GET, f'https://www.pdga.com/player/{pdga_number}',
                      body='<div class="pane-content">'
                           '  <ul class="player-info info-list">'
                           '    <li class="location">'
                           '      <strong>Location:</strong>'
                           '      <a href="/players?City=M%C3%A1laga&amp;Country=ES">Málaga, Málaga, Spain</a>'
                           '    </li>'
                           '    <li class="classification">'
                           '      <strong>Classification: </strong>'
                           '        Amateur'
                           '    </li>'
                           '    <li class="join-date">'
                           '      <strong>Member Since:</strong>'
                           '        2018'
                           '      </li>'
                           '    <li class="membership-status">'
                           '      <strong>Membership Status: </strong>'
                           '      <a href="/membership">Current</a>'
                           '      <small class="membership-expiration-date">(until 31-Dec-2021)</small>'
                           '    </li>'
                           '    <li class="current-rating">'
                           '      <strong>Current Rating:</strong> 895'
                           '      <small class="rating-date">(as of 11-Aug-2020)</small>'
                           '    </li>'
                           '    <li class="career-events disclaimer" title="Singles-format tournaments played.">'
                           '      <strong>Career Events:</strong>'
                           '      12'
                           '    </li>'
                           '    <li class="next-event">'
                           '      <strong>Next Event:</strong>'
                           '      <a href="/tour/event/333">Tremonia Series #3</a>'
                           '    </li>'
                           '  </ul>'
                           '</div>')

    def fake_pdga_player_page_with_upcoming_events(self, pdga_number):
        responses.add(responses.GET, f'https://www.pdga.com/player/{pdga_number}',
                      body='<div class="pane-content">'
                           '  <ul class="player-info info-list">'
                           '    <li class="location">'
                           '      <strong>Location:</strong>'
                           '      <a href="/players?City=M%C3%A1laga&amp;Country=ES">Málaga, Málaga, Spain</a>'
                           '    </li>'
                           '    <li class="classification">'
                           '      <strong>Classification: </strong>'
                           '        Amateur'
                           '    </li>'
                           '    <li class="join-date">'
                           '      <strong>Member Since:</strong>'
                           '        2018'
                           '      </li>'
                           '    <li class="membership-status">'
                           '      <strong>Membership Status: </strong>'
                           '      <a href="/membership">Current</a>'
                           '      <small class="membership-expiration-date">(until 31-Dec-2021)</small>'
                           '    </li>'
                           '    <li class="current-rating">'
                           '      <strong>Current Rating:</strong> 895'
                           '      <small class="rating-date">(as of 11-Aug-2020)</small>'
                           '    </li>'
                           '    <li class="career-events disclaimer" title="Singles-format tournaments played.">'
                           '      <strong>Career Events:</strong>'
                           '      12'
                           '    </li>'
                           '    <li class="upcoming-events">'
                           '      <details open="">'
                           '        <summary>'
                           '          <strong>Upcoming Events</strong>'
                           '        </summary>'
                           '        <ul>'
                           '          <li>'
                           '              <a href="/tour/event/333">Tremonia Series #3</a>'
                           '          </li>'
                           '          <li>'
                           '              <a href="/tour/event/444">Tremonia Series #4</a>'
                           '          </li>'
                           '        </ul>'
                           '      </details>'
                           '    </li>'
                           '  </ul>'
                           '</div>')
