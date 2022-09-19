from datetime import date

import responses

from dgf import german_tour
from dgf.models import Tournament, Friend, Attendance
from dgf.test.german_tour.parent import GermanTourTest
from dgf.test.german_tour.responses import add_list_page, add_details_page, add_attendance_page, add_rating_page

APRIL_2 = date(year=3000, month=4, day=2)
JULY_24 = date(year=3000, month=7, day=24)
JULY_25 = date(year=3000, month=7, day=25)
JULY_26 = date(year=3000, month=7, day=26)


class GermanTourAttendanceTest(GermanTourTest):

    def setUp(self):
        super().setUp()
        Attendance.objects.all().delete()

        self.manolo = Friend.objects.create(username='manolo', gt_number=1922)
        add_rating_page(1922, [])  # we don't need ratings for attendance tests

    @responses.activate
    def test_tournament_without_attendance_and_with_empty_attendance(self):
        add_list_page([111, 222])
        add_details_page(111, 'Test Tournament #1', '24.07.3000 - 24.07.3000')
        add_attendance_page(111, None)
        add_details_page(222, 'Test Tournament #2', '25.07.3000 - 26.07.3000')
        add_attendance_page(222, [None, None, None])

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(2)
        self.assert_attendance_amount(0)

    @responses.activate
    def test_tournament_without_attendance_and_with_empty_attendance_existing_tournaments(self):
        Tournament.objects.create(gt_id=111, name='Test Tournament #1', begin=JULY_24, end=JULY_24)
        Tournament.objects.create(gt_id=222, name='Test Tournament #2', begin=JULY_25, end=JULY_26)

        add_list_page([111, 222])
        add_details_page(111, 'Test Tournament #1', '24.07.3000 - 24.07.3000')
        add_attendance_page(111, None)
        add_details_page(222, 'Test Tournament #2', '25.07.3000 - 26.07.3000')
        add_attendance_page(222, [None, None, None])

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(2)
        self.assert_attendance_amount(0)

    @responses.activate
    def test_tournament_without_friends_in_attendance(self):
        add_list_page([111])
        add_details_page(111, 'Test Tournament #1', '24.07.3000 - 24.07.3000')
        add_attendance_page(111, [1234, 5678])

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(1)
        self.assert_attendance_amount(0)

    @responses.activate
    def test_tournament_with_attendance_no_tournaments(self):
        add_list_page([111])
        add_details_page(111, 'Test Tournament #1', '24.07.3000 - 24.07.3000')
        add_attendance_page(111, [1922, 1234])

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(111, 'Test Tournament #1', JULY_24, JULY_24,
                                      'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=111')
        self.assert_attendance_amount(1)
        self.assert_attendance(self.manolo, [111])

    @responses.activate
    def test_tournament_with_attendance_no_tournaments_with_different_attendance_format(self):
        add_list_page([111])
        add_details_page(111, 'Test Tournament #1', '24.07.3000 - 24.07.3000')
        add_attendance_page(111, [1922, 1234], other_format=True)

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(111, 'Test Tournament #1', JULY_24, JULY_24,
                                      'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=111')
        self.assert_attendance_amount(1)
        self.assert_attendance(self.manolo, [111])

    @responses.activate
    def test_tournament_with_attendance_existing_tournaments(self):
        Tournament.objects.create(gt_id=111, name='Test Tournament #1', begin=JULY_24, end=JULY_24)

        add_list_page([111])
        add_details_page(111, 'Test Tournament #1', '24.07.3000 - 24.07.3000')
        add_attendance_page(111, [1922, 1234])

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(111, 'Test Tournament #1', JULY_24, JULY_24,
                                      'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=111')
        self.assert_attendance_amount(1)
        self.assert_attendance(self.manolo, [111])

    @responses.activate
    def test_tournament_with_attendance_existing_attendance_existing_tournaments(self):
        tournament_1 = Tournament.objects.create(gt_id=111, name='Test Tournament #1', begin=JULY_24, end=JULY_24)
        Attendance.objects.create(friend=self.manolo, tournament=tournament_1)

        add_list_page([111])
        add_details_page(111, 'Test Tournament #1', '24.07.3000 - 24.07.3000')
        add_attendance_page(111, [1922, 1234])

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(111, 'Test Tournament #1', JULY_24, JULY_24,
                                      'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=111')
        self.assert_attendance_amount(1)
        self.assert_attendance(self.manolo, [111])

    @responses.activate
    def test_tournament_with_attendance_existing_attendance_adding_more_tournaments(self):
        tournament_1 = Tournament.objects.create(gt_id=111, name='Test Tournament #1', begin=JULY_24, end=JULY_24)
        Attendance.objects.create(friend=self.manolo, tournament=tournament_1)

        add_list_page([111, 222])
        add_details_page(111, 'Test Tournament #1', '24.07.3000 - 24.07.3000')
        add_attendance_page(111, [1922])
        add_details_page(222, 'Test Tournament #2', '25.07.3000 - 26.07.3000')
        add_attendance_page(222, [1922, 1234])

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(2)
        self.assert_tournament_exists(111, 'Test Tournament #1', JULY_24, JULY_24,
                                      'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=111')
        self.assert_tournament_exists(222, 'Test Tournament #2', JULY_25, JULY_26,
                                      'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=222')
        self.assert_attendance_amount(2)
        self.assert_attendance(self.manolo, [111, 222])

    @responses.activate
    def test_tournament_with_attendance_existing_attendance_adding_more_existing_tournaments(self):
        tournament_1 = Tournament.objects.create(gt_id=111, name='Test Tournament #1', begin=JULY_24, end=JULY_24)
        Tournament.objects.create(gt_id=222, name='Test Tournament #2', begin=JULY_25, end=JULY_26)
        Attendance.objects.create(friend=self.manolo, tournament=tournament_1)

        add_list_page([111, 222])
        add_details_page(111, 'Test Tournament #1', '24.07.3000 - 24.07.3000')
        add_attendance_page(111, [1922])
        add_details_page(222, 'Test Tournament #2', '25.07.3000 - 26.07.3000')
        add_attendance_page(222, [1922, 1234])

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(2)
        self.assert_tournament_exists(111, 'Test Tournament #1', JULY_24, JULY_24,
                                      'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=111')
        self.assert_tournament_exists(222, 'Test Tournament #2', JULY_25, JULY_26,
                                      'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=222')
        self.assert_attendance_amount(2)
        self.assert_attendance(self.manolo, [111, 222])

    @responses.activate
    def test_tournament_name_change(self):
        Tournament.objects.create(gt_id=111, name='Test Tournament #1', begin=JULY_24, end=JULY_24)

        add_list_page([111])
        add_details_page(111, 'Test Tournament #111', '24.07.3000 - 24.07.3000')
        add_attendance_page(111, None)

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(111, 'Test Tournament #111', JULY_24, JULY_24,
                                      'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=111')
        self.assert_attendance_amount(0)

    @responses.activate
    def test_tournament_date_change(self):
        Tournament.objects.create(gt_id=111, name='Test Tournament #1', begin=JULY_24, end=JULY_24)

        add_list_page([111])
        add_details_page(111, 'Test Tournament #1', '02.04.3000 - 02.04.3000')
        add_attendance_page(111, None)

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(111, 'Test Tournament #1', APRIL_2, APRIL_2,
                                      'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=111')
        self.assert_attendance_amount(0)

    @responses.activate
    def test_canceled_tournament_non_existing(self):
        Tournament.objects.create(gt_id=111, name='Test Tournament #1', begin=JULY_24, end=JULY_24)

        add_list_page([111, 222])
        add_details_page(111, 'Test Tournament #1', '24.07.3000 - 24.07.3000')
        add_attendance_page(111, None)
        add_details_page(222, 'Test Tournament #2', '25.07.3000 - 26.07.3000', canceled=True)

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(111, 'Test Tournament #1', JULY_24, JULY_24,
                                      'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=111')
        self.assert_tournament_does_not_exists(222)

    @responses.activate
    def test_canceled_tournament_with_existing_tournament_without_attendance(self):
        Tournament.objects.create(gt_id=111, name='Test Tournament #1', begin=JULY_24, end=JULY_24)
        Tournament.objects.create(gt_id=222, name='Test Tournament #2', begin=JULY_25, end=JULY_26)

        add_list_page([111, 222])
        add_details_page(111, 'Test Tournament #1', '24.07.3000 - 24.07.3000')
        add_attendance_page(111, None)
        add_details_page(222, 'Test Tournament #2', '25.07.3000 - 26.07.3000', canceled=True)

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(111, 'Test Tournament #1', JULY_24, JULY_24,
                                      'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=111')
        self.assert_tournament_does_not_exists(222)

    @responses.activate
    def test_canceled_tournament_with_existing_tournament_with_attendance(self):
        tournament_1 = Tournament.objects.create(gt_id=111, name='Test Tournament #1', begin=JULY_24, end=JULY_24)
        tournament_2 = Tournament.objects.create(gt_id=222, name='Test Tournament #2', begin=JULY_25, end=JULY_26)
        Attendance.objects.create(friend=self.manolo, tournament=tournament_1)
        Attendance.objects.create(friend=self.manolo, tournament=tournament_2)

        add_list_page([111, 222])
        add_details_page(111, 'Test Tournament #1', '24.07.3000 - 24.07.3000')
        add_attendance_page(111, None)
        add_details_page(222, 'Test Tournament #2', '25.07.3000 - 26.07.3000', canceled=True)

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(111, 'Test Tournament #1', JULY_24, JULY_24,
                                      'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=111')
        self.assert_tournament_does_not_exists(222)

    @responses.activate
    def test_tremonia_series_tournament(self):
        add_list_page([111])
        add_details_page(111, 'Tremonia Series #1', '24.07.3000 - 24.07.3000')

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(0)
        self.assert_tournament_does_not_exists(111)

    @responses.activate
    def test_tremonia_series_tournament_with_existing_tournament(self):
        Tournament.objects.create(metrix_id=111, name='Tremonia Series #1', begin=JULY_24, end=JULY_24)

        add_list_page([111])
        add_details_page(111, 'Tremonia Series #11', '24.07.3000 - 24.07.3000')

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(None, 'Tremonia Series #1', JULY_24, JULY_24,  # name is not changed
                                      'https://discgolfmetrix.com/111',
                                      metrix_id=111)

    @responses.activate
    def test_update_pdga_id(self):
        Tournament.objects.create(gt_id=111, name='PDGA Tournament #1', begin=JULY_24, end=JULY_24)
        add_list_page([111])
        add_details_page(111, 'PDGA Tournament #1', '24.07.3000 - 24.07.3000', pdga_id=1111)
        add_attendance_page(111, None)

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(111, 'PDGA Tournament #1', JULY_24, JULY_24,
                                      'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=111',
                                      pdga_id=1111)

    @responses.activate
    def test_pdga_tournament_non_existing_tournament(self):
        add_list_page([111])
        add_details_page(111, 'PDGA Tournament #1', '24.07.3000 - 24.07.3000', pdga_id=1111)
        add_attendance_page(111, None)

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(111, 'PDGA Tournament #1', JULY_24, JULY_24,
                                      'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=111',
                                      pdga_id=1111)

    @responses.activate
    def test_pdga_tournament_existing_tournament_without_pdga_status(self):
        Tournament.objects.create(pdga_id=1111, name='PDGA Tournament #1', begin=JULY_24, end=JULY_24)

        add_list_page([111])
        add_details_page(111, 'PDGA Tournament #1', '24.07.3000 - 24.07.3000')
        add_attendance_page(111, None)

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(111, 'PDGA Tournament #1', JULY_24, JULY_24,
                                      'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=111',
                                      pdga_id=1111)

    @responses.activate
    def test_pdga_tournament_existing_tournament_with_empty_pdga_status(self):
        Tournament.objects.create(pdga_id=1111, name='PDGA Tournament #1', begin=JULY_24, end=JULY_24)

        add_list_page([111])
        add_details_page(111, 'PDGA Tournament #1', '24.07.3000 - 24.07.3000', pdga_id=0)
        add_attendance_page(111, None)

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(111, 'PDGA Tournament #1', JULY_24, JULY_24,
                                      'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=111',
                                      pdga_id=1111)

    @responses.activate
    def test_pdga_tournament_existing_tournament_with_pdga_id_in_pdga_status(self):
        Tournament.objects.create(pdga_id=1111, name='PDGA Tournament #1', begin=JULY_24, end=JULY_24)

        add_list_page([111])
        add_details_page(111, 'PDGA Tournament #1', '24.07.3000 - 24.07.3000', pdga_id=1111)
        add_attendance_page(111, None)

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(111, 'PDGA Tournament #1', JULY_24, JULY_24,
                                      'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=111',
                                      pdga_id=1111)

    @responses.activate
    def test_pdga_tournament_existing_tournament_with_pdga_id_in_pdga_status_with_gt_id(self):
        Tournament.objects.create(gt_id=111, pdga_id=1111, name='PDGA Tournament #1', begin=JULY_24, end=JULY_24)

        add_list_page([111])
        add_details_page(111, 'PDGA Tournament #1', '24.07.3000 - 24.07.3000', pdga_id=1111)
        add_attendance_page(111, None)

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(111, 'PDGA Tournament #1', JULY_24, JULY_24,
                                      'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=111',
                                      pdga_id=1111)

    @responses.activate
    def test_pdga_tournament_existing_tournament_with_pdga_id_with_attendance(self):
        tournament_1 = Tournament.objects.create(pdga_id=1111, name='PDGA Tournament #1', begin=JULY_24, end=JULY_24)
        Attendance.objects.create(friend=self.manolo, tournament=tournament_1)

        add_list_page([111])
        add_details_page(111, 'PDGA Tournament #1', '24.07.3000 - 24.07.3000', pdga_id=1111)
        add_attendance_page(111, [1922, 1234])

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(111, 'PDGA Tournament #1', JULY_24, JULY_24,
                                      'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=111',
                                      pdga_id=1111)
        self.assert_attendance_amount(1)
        self.assert_attendance(self.manolo, [111])

    @responses.activate
    def test_pdga_tournament_with_existing_gt_and_pdga_tournaments_already(self):
        Tournament.objects.create(gt_id=111, name='PDGA Tournament #1', begin=JULY_24, end=JULY_24)
        Tournament.objects.create(pdga_id=1111, name='1. PDGA Tournament', begin=JULY_24, end=JULY_24)

        add_list_page([111])
        add_details_page(111, 'PDGA Tournament #1', '24.07.3000 - 24.07.3000', pdga_id=1111)
        add_attendance_page(111, None)

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(111, 'PDGA Tournament #1', JULY_24, JULY_24,
                                      'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=111',
                                      pdga_id=1111)

    @responses.activate
    def test_attendance_from_one_tournament(self):
        tournament_1 = Tournament.objects.create(gt_id=111, name='Test Tournament #1', begin=JULY_24, end=JULY_24)

        add_list_page([111])
        add_details_page(111, 'Test Tournament #1', '24.07.3000 - 24.07.3000')
        add_attendance_page(111, [1922, 1234])

        german_tour.update_tournament_attendance(tournament_1)

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(111, 'Test Tournament #1', JULY_24, JULY_24,
                                      'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=111')
        self.assert_attendance_amount(1)
        self.assert_attendance(self.manolo, [111])

    def assert_attendance_amount(self, amount):
        self.assertEqual(Attendance.objects.all().count(), amount, f'there should be {amount} Attendance objects')

    def assert_attendance(self, friend, expected_gt_ids):
        actual_gt_ids = list(friend.attendance.values_list('tournament__gt_id', flat=True))
        self.assertEqual(actual_gt_ids, expected_gt_ids, 'expected GT IDs do not match')
