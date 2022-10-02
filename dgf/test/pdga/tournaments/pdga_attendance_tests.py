import responses

from dgf import pdga
from dgf.models import Friend, Attendance, Tournament
from dgf.test.pdga.tournaments.pdga_tournament_test import PdgaTournamentTest, JULY_24, JULY_25, JULY_26, APRIL_2
from dgf.test.pdga.tournaments.responses import add_tournament_data, add_player_page_with_upcoming_events, \
    add_player_page_with_next_event, add_player_page_without_events
from dgf_cms.settings import PDGA_EVENT_URL


class PdgaAttendanceTest(PdgaTournamentTest):

    @responses.activate
    def setUp(self):
        super().setUp()
        Attendance.objects.all().delete()

    def test_no_pdga_number_no_attendance(self):
        manolo = Friend.objects.create(username='manolo')

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        self.assert_tournament_amount(0)
        self.assert_attendance_amount(0)

    def test_no_pdga_number_but_attendance(self):
        manolo = Friend.objects.create(username='manolo')
        ts3 = Tournament.objects.create(pdga_id=3333, name='Tremonia Series #3', begin=JULY_24, end=JULY_24)
        Attendance.objects.create(friend=manolo, tournament=ts3)

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(3333, 'Tremonia Series #3', JULY_24, JULY_24, PDGA_EVENT_URL.format(3333))

        self.assert_attendance_amount(1)
        self.assert_attendance(manolo, [3333])

    @responses.activate
    def test_without_events_no_attendance(self):
        manolo = Friend.objects.create(username='manolo', pdga_number=111828)

        add_player_page_without_events(111828)

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        self.assert_tournament_amount(0)
        self.assert_attendance_amount(0)

    @responses.activate
    def test_without_events_but_attendance(self):
        manolo = Friend.objects.create(username='manolo', pdga_number=111828)
        ts3 = Tournament.objects.create(pdga_id=3333, name='Tremonia Series #3', begin=JULY_24, end=JULY_24)
        Attendance.objects.create(friend=manolo, tournament=ts3)

        add_player_page_without_events(111828)

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(3333, 'Tremonia Series #3', JULY_24, JULY_24, PDGA_EVENT_URL.format(3333))

        self.assert_attendance_amount(1)
        self.assert_attendance(manolo, [3333])

    @responses.activate
    def test_next_event_no_attendance_no_tournament(self):
        manolo = Friend.objects.create(username='manolo', pdga_number=111828)

        add_player_page_with_next_event(111828, 3333)
        add_tournament_data('3333', 'Tremonia Series #3', '2021-07-24', '2021-07-24')

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(3333, 'Tremonia Series #3', JULY_24, JULY_24, PDGA_EVENT_URL.format(3333))

        self.assert_attendance_amount(1)
        self.assert_attendance(manolo, [3333])

    @responses.activate
    def test_next_event_no_attendance_existing_tournament(self):
        manolo = Friend.objects.create(username='manolo', pdga_number=111828)
        Tournament.objects.create(pdga_id=3333, name='Tremonia Series #3', begin=JULY_24, end=JULY_24)

        add_player_page_with_next_event(111828, 3333)
        add_tournament_data('3333', 'Tremonia Series #3', '2021-07-24', '2021-07-24')

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(3333, 'Tremonia Series #3', JULY_24, JULY_24, PDGA_EVENT_URL.format(3333))

        self.assert_attendance_amount(1)
        self.assert_attendance(manolo, [3333])

    @responses.activate
    def test_next_event_existing_attendance_existing_tournament(self):
        manolo = Friend.objects.create(username='manolo', pdga_number=111828)
        ts3 = Tournament.objects.create(pdga_id=3333, name='Tremonia Series #3', begin=JULY_24, end=JULY_24)
        Attendance.objects.create(friend=manolo, tournament=ts3)

        add_player_page_with_next_event(111828, 3333)
        add_tournament_data('3333', 'Tremonia Series #3', '2021-07-24', '2021-07-24')

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(3333, 'Tremonia Series #3', JULY_24, JULY_24, PDGA_EVENT_URL.format(3333))

        self.assert_attendance_amount(1)
        self.assert_attendance(manolo, [3333])

    @responses.activate
    def test_upcoming_events_no_attendance_no_tournaments(self):
        manolo = Friend.objects.create(username='manolo', pdga_number=111828)

        add_player_page_with_upcoming_events(111828, [3333, 4444])
        add_tournament_data('3333', 'Tremonia Series #3', '2021-07-24', '2021-07-24')
        add_tournament_data('4444', 'Tremonia Series #4', '2021-07-25', '2021-07-26')

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        self.assert_tournament_amount(2)
        self.assert_tournament_exists(3333, 'Tremonia Series #3', JULY_24, JULY_24, PDGA_EVENT_URL.format(3333))
        self.assert_tournament_exists(4444, 'Tremonia Series #4', JULY_25, JULY_26, PDGA_EVENT_URL.format(4444))

        self.assert_attendance_amount(2)
        self.assert_attendance(manolo, [3333, 4444])

    @responses.activate
    def test_upcoming_events_no_attendance_existing_tournaments(self):
        manolo = Friend.objects.create(username='manolo', pdga_number=111828)
        Tournament.objects.create(pdga_id=3333, name='Tremonia Series #3', begin=JULY_24, end=JULY_24)
        Tournament.objects.create(pdga_id=4444, name='Tremonia Series #4', begin=JULY_25, end=JULY_26)

        add_player_page_with_upcoming_events(111828, [3333, 4444])
        add_tournament_data('3333', 'Tremonia Series #3', '2021-07-24', '2021-07-24')
        add_tournament_data('4444', 'Tremonia Series #4', '2021-07-25', '2021-07-26')

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        self.assert_tournament_amount(2)
        self.assert_tournament_exists(3333, 'Tremonia Series #3', JULY_24, JULY_24, PDGA_EVENT_URL.format(3333))
        self.assert_tournament_exists(4444, 'Tremonia Series #4', JULY_25, JULY_26, PDGA_EVENT_URL.format(4444))

        self.assert_attendance_amount(2)
        self.assert_attendance(manolo, [3333, 4444])

    @responses.activate
    def test_upcoming_events_existing_attendance_existing_tournaments(self):
        manolo = Friend.objects.create(username='manolo', pdga_number=111828)
        ts3 = Tournament.objects.create(pdga_id=3333, name='Tremonia Series #3', begin=JULY_24, end=JULY_24)
        ts4 = Tournament.objects.create(pdga_id=4444, name='Tremonia Series #4', begin=JULY_25, end=JULY_26)
        Attendance.objects.create(friend=manolo, tournament=ts3)
        Attendance.objects.create(friend=manolo, tournament=ts4)

        add_player_page_with_upcoming_events(111828, [3333, 4444])
        add_tournament_data('3333', 'Tremonia Series #3', '2021-07-24', '2021-07-24')
        add_tournament_data('4444', 'Tremonia Series #4', '2021-07-25', '2021-07-26')

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        self.assert_tournament_amount(2)
        self.assert_tournament_exists(3333, 'Tremonia Series #3', JULY_24, JULY_24, PDGA_EVENT_URL.format(3333))
        self.assert_tournament_exists(4444, 'Tremonia Series #4', JULY_25, JULY_26, PDGA_EVENT_URL.format(4444))

        self.assert_attendance_amount(2)
        self.assert_attendance(manolo, [3333, 4444])

    @responses.activate
    def test_upcoming_events_name_change(self):
        manolo = Friend.objects.create(username='manolo', pdga_number=111828)
        Tournament.objects.create(pdga_id=3333, name='Tremonia Series #3', begin=JULY_24, end=JULY_24)

        add_player_page_with_upcoming_events(111828, [3333])
        add_tournament_data('3333', 'TS #3', '2021-07-24', '2021-07-24')

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(3333, 'TS #3', JULY_24, JULY_24, PDGA_EVENT_URL.format(3333))

    @responses.activate
    def test_upcoming_events_date_change(self):
        manolo = Friend.objects.create(username='manolo', pdga_number=111828)
        Tournament.objects.create(pdga_id=3333, name='Tremonia Series #3', begin=JULY_24, end=JULY_24)

        add_player_page_with_upcoming_events(111828, [3333])
        add_tournament_data('3333', 'Tremonia Series #3', '2021-04-02', '2021-04-02')

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(3333, 'Tremonia Series #3', APRIL_2, APRIL_2, PDGA_EVENT_URL.format(3333))

    def assert_attendance_amount(self, amount):
        self.assertEqual(Attendance.objects.all().count(), amount, f'there should be {amount} Attendance objects')

    def assert_attendance(self, friend, expected_pdga_ids):
        actual_gt_ids = list(friend.attendance.values_list('tournament__pdga_id', flat=True))
        self.assertEqual(actual_gt_ids, expected_pdga_ids, 'expected PDGA IDs do not match')
