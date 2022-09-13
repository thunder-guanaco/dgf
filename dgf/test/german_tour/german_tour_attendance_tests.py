from datetime import date

import responses
from django.test import TestCase

from dgf import german_tour
from dgf.models import Tournament, Friend, Attendance
from dgf_cms.settings import GT_LIST_PAGE, GT_ATTENDANCE_PAGE

APRIL_2 = date(year=2021, month=4, day=2)
JULY_24 = date(year=2021, month=7, day=24)
JULY_25 = date(year=2021, month=7, day=25)
JULY_26 = date(year=2021, month=7, day=26)
JULY_27 = date(year=2021, month=7, day=27)


class GermanTourAttendanceTest(TestCase):

    def setUp(self):
        Friend.objects.all().delete()
        Attendance.objects.all().delete()
        Tournament.objects.all().delete()

    @responses.activate
    def test_tournament_without_attendance_and_with_empty_attendance(self):
        add_tournament_list()
        add_tournament_without_attendance_list(333)
        add_tournament_with_empty_attendance_list(444)
        Friend.objects.create(username='manolo', gt_number=1922)

        german_tour.update_all_tournaments_attendance()

        attendance_list = list(Attendance.objects.all())
        self.assertListEqual(attendance_list, [])

    @responses.activate
    def test_tournament_without_attendance_and_with_empty_attendance_existing_tournaments(self):
        add_tournament_list()
        add_tournament_with_empty_attendance_list(333)
        add_tournament_without_attendance_list(444)
        Tournament.objects.create(gt_id=333, name='Test Tournament #3', begin=JULY_24, end=JULY_24)
        Tournament.objects.create(gt_id=444, name='Test Tournament #4', begin=JULY_24, end=JULY_25)
        Friend.objects.create(username='manolo', gt_number=1922)

        german_tour.update_all_tournaments_attendance()

        attendance_list = list(Attendance.objects.all())
        self.assertListEqual(attendance_list, [])

    @responses.activate
    def test_tournament_with_attendance_no_tournaments(self):
        add_tournament_list()
        add_tournament_attendance_list(333)
        add_tournament_attendance_list(444)
        manolo = Friend.objects.create(username='manolo', gt_number=1922)

        german_tour.update_all_tournaments_attendance()

        attendance_list = Attendance.objects.filter(friend=manolo)
        self.assertEqual(len(attendance_list), 2)

        attendance_tournament_3 = attendance_list.get(tournament__gt_id=333)
        self.assertEqual(attendance_tournament_3.tournament.name, 'Test Tournament #3')
        self.assertEqual(attendance_tournament_3.tournament.url,
                         'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=333')
        self.assertEqual(attendance_tournament_3.tournament.begin, JULY_24)
        self.assertEqual(attendance_tournament_3.tournament.end, JULY_24)
        self.assertEqual(attendance_tournament_3.friend, manolo)

        attendance_tournament_4 = attendance_list.get(tournament__gt_id=444)
        self.assertEqual(attendance_tournament_4.tournament.name, 'Test Tournament #4')
        self.assertEqual(attendance_tournament_4.tournament.url,
                         'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=444')
        self.assertEqual(attendance_tournament_4.tournament.begin, JULY_24)
        self.assertEqual(attendance_tournament_4.tournament.end, JULY_25)
        self.assertEqual(attendance_tournament_4.friend, manolo)

    @responses.activate
    def test_tournament_with_attendance_no_tournaments_with_different_attendance_formats(self):
        add_tournament_list()
        add_tournament_attendance_list(333)
        add_tournament_attendance_list_with_other_format(444)
        manolo = Friend.objects.create(username='manolo', gt_number=1922)

        german_tour.update_all_tournaments_attendance()

        attendance_list = Attendance.objects.filter(friend=manolo)
        self.assertEqual(len(attendance_list), 2)

        attendance_tournament_3 = attendance_list.get(tournament__gt_id=333)
        self.assertEqual(attendance_tournament_3.tournament.name, 'Test Tournament #3')
        self.assertEqual(attendance_tournament_3.tournament.url,
                         'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=333')
        self.assertEqual(attendance_tournament_3.tournament.begin, JULY_24)
        self.assertEqual(attendance_tournament_3.tournament.end, JULY_24)
        self.assertEqual(attendance_tournament_3.friend, manolo)

        attendance_tournament_4 = attendance_list.get(tournament__gt_id=444)
        self.assertEqual(attendance_tournament_4.tournament.name, 'Test Tournament #4')
        self.assertEqual(attendance_tournament_4.tournament.url,
                         'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=444')
        self.assertEqual(attendance_tournament_4.tournament.begin, JULY_24)
        self.assertEqual(attendance_tournament_4.tournament.end, JULY_25)
        self.assertEqual(attendance_tournament_4.friend, manolo)

    @responses.activate
    def test_tournament_with_attendance_existing_tournaments(self):
        add_tournament_list()
        add_tournament_attendance_list(333)
        add_tournament_attendance_list(444)
        manolo = Friend.objects.create(username='manolo', gt_number=1922)
        Tournament.objects.create(gt_id=333, name='Test Tournament #3', begin=JULY_24, end=JULY_24)
        Tournament.objects.create(gt_id=444, name='Test Tournament #4', begin=JULY_24, end=JULY_25)

        german_tour.update_all_tournaments_attendance()

        attendance_list = Attendance.objects.filter(friend=manolo)
        self.assertEqual(len(attendance_list), 2)

        attendance_tournament_3 = attendance_list.get(tournament__gt_id=333)
        self.assertEqual(attendance_tournament_3.tournament.name, 'Test Tournament #3')
        self.assertEqual(attendance_tournament_3.tournament.url,
                         'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=333')
        self.assertEqual(attendance_tournament_3.tournament.begin, JULY_24)
        self.assertEqual(attendance_tournament_3.tournament.end, JULY_24)
        self.assertEqual(attendance_tournament_3.friend, manolo)

        attendance_tournament_4 = attendance_list.get(tournament__gt_id=444)
        self.assertEqual(attendance_tournament_4.tournament.name, 'Test Tournament #4')
        self.assertEqual(attendance_tournament_4.tournament.url,
                         'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=444')
        self.assertEqual(attendance_tournament_4.tournament.begin, JULY_24)
        self.assertEqual(attendance_tournament_4.tournament.end, JULY_25)
        self.assertEqual(attendance_tournament_4.friend, manolo)

    @responses.activate
    def test_tournament_with_attendance_existing_attendance_existing_tournaments(self):
        add_tournament_list()
        add_tournament_attendance_list(333)
        add_tournament_attendance_list(444)
        manolo = Friend.objects.create(username='manolo', gt_number=1922)
        tournament_3 = Tournament.objects.create(gt_id=333, name='Test Tournament #3', begin=JULY_24, end=JULY_24)
        tournament_4 = Tournament.objects.create(gt_id=444, name='Test Tournament #4', begin=JULY_24, end=JULY_25)
        Attendance.objects.create(friend=manolo, tournament=tournament_3)
        Attendance.objects.create(friend=manolo, tournament=tournament_4)

        german_tour.update_all_tournaments_attendance()

        attendance_list = Attendance.objects.filter(friend=manolo)
        self.assertEqual(len(attendance_list), 2)

        attendance_tournament_3 = attendance_list.get(tournament__gt_id=333)
        self.assertEqual(attendance_tournament_3.tournament, tournament_3)
        self.assertEqual(attendance_tournament_3.friend, manolo)

        attendance_tournament_4 = attendance_list.get(tournament__gt_id=444)
        self.assertEqual(attendance_tournament_4.tournament, tournament_4)
        self.assertEqual(attendance_tournament_4.friend, manolo)

    @responses.activate
    def test_tournament_with_attendance_existing_attendance_adding_more_existing_tournaments(self):
        add_tournament_list()
        add_tournament_attendance_list(333)
        add_tournament_attendance_list(444)
        manolo = Friend.objects.create(username='manolo', gt_number=1922)
        tournament_3 = Tournament.objects.create(gt_id=333, name='Test Tournament #3', begin=JULY_24, end=JULY_24)
        tournament_4 = Tournament.objects.create(gt_id=444, name='Test Tournament #4', begin=JULY_24, end=JULY_25)
        Attendance.objects.create(friend=manolo, tournament=tournament_3)

        german_tour.update_all_tournaments_attendance()

        attendance_list = Attendance.objects.filter(friend=manolo)
        self.assertEqual(len(attendance_list), 2)

        attendance_tournament_3 = attendance_list.get(tournament__gt_id=333)
        self.assertEqual(attendance_tournament_3.tournament, tournament_3)
        self.assertEqual(attendance_tournament_3.friend, manolo)

        attendance_tournament_4 = attendance_list.get(tournament__gt_id=444)
        self.assertEqual(attendance_tournament_4.tournament, tournament_4)
        self.assertEqual(attendance_tournament_4.friend, manolo)

    @responses.activate
    def test_tournament_name_change(self):
        add_tournament_list()
        add_tournament_attendance_list(333)
        add_tournament_attendance_list(444)

        Tournament.objects.create(gt_id=333, name='Test Tournament #33', begin=JULY_24, end=JULY_24)
        Tournament.objects.create(gt_id=444, name='Test Tournament #43', begin=JULY_24, end=JULY_25)

        german_tour.update_all_tournaments_attendance()

        tournament_3 = Tournament.objects.get(gt_id=333)
        self.assertEqual(tournament_3.name, 'Test Tournament #3')

        tournament_4 = Tournament.objects.get(gt_id=444)
        self.assertEqual(tournament_4.name, 'Test Tournament #4')

    @responses.activate
    def test_tournament_date_change(self):
        add_tournament_list()
        add_tournament_attendance_list(333)
        add_tournament_attendance_list(444)

        Tournament.objects.create(gt_id=333, name='Test Tournament #3', begin=APRIL_2, end=APRIL_2)
        Tournament.objects.create(gt_id=444, name='Test Tournament #4', begin=JULY_24, end=JULY_24)

        german_tour.update_all_tournaments_attendance()

        tournament_3 = Tournament.objects.get(gt_id=333)
        self.assertEqual(tournament_3.begin, JULY_24)
        self.assertEqual(tournament_3.end, JULY_24)

        tournament_4 = Tournament.objects.get(gt_id=444)
        self.assertEqual(tournament_4.begin, JULY_24)
        self.assertEqual(tournament_4.end, JULY_25)

    @responses.activate
    def test_canceled_tournament_non_existing(self):
        add_tournament_list_with_canceled_event()
        add_tournament_with_empty_attendance_list(666)

        german_tour.update_all_tournaments_attendance()

        tournament_5 = list(Tournament.objects.filter(gt_id=555))
        self.assertEqual(tournament_5, [])

        tournament_6 = Tournament.objects.get(gt_id=666)
        self.assertEqual(tournament_6.name, 'Test Tournament #6')
        self.assertEqual(tournament_6.begin, JULY_25)
        self.assertEqual(tournament_6.end, JULY_25)

    @responses.activate
    def test_canceled_tournament_with_existing_tournament_without_attendance(self):
        add_tournament_list_with_canceled_event()
        add_tournament_with_empty_attendance_list(666)

        Tournament.objects.create(gt_id=555, name='Test Tournament #5', begin=JULY_24, end=JULY_24)
        Tournament.objects.create(gt_id=666, name='Test Tournament #6', begin=JULY_25, end=JULY_25)

        german_tour.update_all_tournaments_attendance()

        tournament_5 = list(Tournament.objects.filter(gt_id=555))
        self.assertEqual(tournament_5, [])

        tournament_6 = Tournament.objects.get(gt_id=666)
        self.assertEqual(tournament_6.name, 'Test Tournament #6')
        self.assertEqual(tournament_6.begin, JULY_25)
        self.assertEqual(tournament_6.end, JULY_25)

    @responses.activate
    def test_canceled_tournament_with_existing_tournament_with_attendance(self):
        add_tournament_list_with_canceled_event()
        add_tournament_with_empty_attendance_list(666)

        manolo = Friend.objects.create(username='manolo', gt_number=1922)
        tournament_5 = Tournament.objects.create(gt_id=555, name='Test Tournament #5', begin=JULY_24, end=JULY_24)
        tournament_6 = Tournament.objects.create(gt_id=666, name='Test Tournament #6', begin=JULY_25, end=JULY_25)
        Attendance.objects.create(friend=manolo, tournament=tournament_5)
        Attendance.objects.create(friend=manolo, tournament=tournament_6)

        german_tour.update_all_tournaments_attendance()

        tournament_5 = list(Tournament.objects.filter(gt_id=555))
        self.assertEqual(tournament_5, [])

        tournament_6 = Tournament.objects.get(gt_id=666)
        self.assertEqual(tournament_6.name, 'Test Tournament #6')
        self.assertEqual(tournament_6.begin, JULY_25)
        self.assertEqual(tournament_6.end, JULY_25)

    @responses.activate
    def test_tremonia_series_tournament(self):
        add_tournament_list_with_tremonia_series_event()
        add_tournament_with_empty_attendance_list(555)
        add_tournament_with_empty_attendance_list(666)

        Friend.objects.create(username='manolo', gt_number=1922)
        Tournament.objects.create(metrix_id=5555, name='Tremonia Series #5', begin=JULY_24, end=JULY_24)

        german_tour.update_all_tournaments_attendance()

        tournament_5 = Tournament.objects.get(name='Tremonia Series #5')  # there's just one
        self.assertEqual(tournament_5.metrix_id, 5555)  # and it's not modified
        self.assertEqual(tournament_5.gt_id, None)  # and it's not modified

        tournament_6 = Tournament.objects.filter(name='Tremonia Series #6')
        self.assertEqual(tournament_6.count(), 0)  # there's no new one

    @responses.activate
    def test_pdga_tournament(self):
        add_tournament_list_with_pdga_event()
        add_tournament_with_empty_attendance_list(777)
        add_tournament_with_empty_attendance_list(888)

        Tournament.objects.create(pdga_id=7777, name='Tremonia Open', begin=JULY_24, end=JULY_25)
        Tournament.objects.create(pdga_id=8888, name='Tremonia Classics', begin=APRIL_2, end=APRIL_2)

        german_tour.update_all_tournaments_attendance()

        tournament_7 = Tournament.objects.get(name='Tremonia Open')
        self.assertEqual(tournament_7.pdga_id, 7777)
        self.assertEqual(tournament_7.gt_id, 777)
        self.assertEqual(tournament_7.url, 'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=777')
        self.assertEqual(tournament_7.begin, JULY_24)
        self.assertEqual(tournament_7.end, JULY_25)

        # the old one (PDGA) and the new one (GT)
        self.assertEqual(Tournament.objects.filter(name='Tremonia Classics').count(), 2)

        pdga_tournament_8 = Tournament.objects.get(pdga_id=8888)
        self.assertEqual(pdga_tournament_8.gt_id, None)
        self.assertEqual(pdga_tournament_8.url, 'https://www.pdga.com/tour/event/8888')
        self.assertEqual(pdga_tournament_8.begin, APRIL_2)
        self.assertEqual(pdga_tournament_8.end, APRIL_2)

        gt_tournament_8 = Tournament.objects.get(gt_id=888)
        self.assertEqual(gt_tournament_8.pdga_id, None)
        self.assertEqual(gt_tournament_8.url, 'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=888')
        self.assertEqual(gt_tournament_8.begin, JULY_26)
        self.assertEqual(gt_tournament_8.end, JULY_27)

    @responses.activate
    def test_existing_pdga_tournament_attendance(self):
        add_tournament_list_with_pdga_event()
        add_tournament_attendance_list(777)
        add_tournament_attendance_list(888)  # not needed for the test

        Friend.objects.create(username='fede', first_name='Fede', gt_number=2106)
        manolo = Friend.objects.create(username='manolo', first_name='Manolo', gt_number=1922)
        tournament_7 = Tournament.objects.create(pdga_id=7777, name='Tremonia Open', begin=JULY_24, end=JULY_25)
        Attendance.objects.create(friend=manolo, tournament=tournament_7)

        german_tour.update_all_tournaments_attendance()

        attendance = set(Attendance.objects.filter(tournament__pdga_id=7777).values_list('friend__username', flat=True))
        self.assertEqual(attendance, {'manolo', 'fede'})
        attendance = set(Attendance.objects.filter(tournament__gt_id=777).values_list('friend__username', flat=True))
        self.assertEqual(attendance, {'manolo', 'fede'})
        attendance = set(Attendance.objects.filter(tournament__gt_id=888).values_list('friend__username', flat=True))
        self.assertEqual(attendance, {'manolo', 'fede'})

    @responses.activate
    def test_attendance_from_one_tournament(self):
        add_tournament_attendance_list(333)
        manolo = Friend.objects.create(username='manolo', gt_number=1922)
        tournament = Tournament.objects.create(gt_id=333, name='Test Tournament #3', begin=JULY_24, end=JULY_24)

        german_tour.update_tournament_attendance(tournament)

        attendance_list = Attendance.objects.filter(friend=manolo)
        self.assertEqual(len(attendance_list), 1)

        attendance_tournament_3 = attendance_list.get(tournament__gt_id=333)
        self.assertEqual(attendance_tournament_3.tournament.name, 'Test Tournament #3')
        self.assertEqual(attendance_tournament_3.tournament.url,
                         'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=333')
        self.assertEqual(attendance_tournament_3.tournament.begin, JULY_24)
        self.assertEqual(attendance_tournament_3.tournament.end, JULY_24)
        self.assertEqual(attendance_tournament_3.friend, manolo)


def add_tournament_list():
    responses.add(responses.GET, GT_LIST_PAGE,
                  body='<body>'
                       '  <table class="table table-sm table-striped dataTable no-footer"'
                       '         id="list_tournaments" role="grid"'
                       '         aria-describedby="list_tournaments_info">'
                       '    <thead></thead>'
                       '    <tbody>'
                       '      <tr class="odd">'
                       '        <td data-sort="Test Tournament #3" id="table_list_tournaments_0_0">'
                       '          <a class="text-muted font-italic"'
                       '            href="https://turniere.discgolf.de/index.php?p=events&amp;sp=view&amp;id=333">'
                       '            Test Tournament #3'
                       '          </a>'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_1">'
                       '          Dortmund'
                       '        </td>'
                       '        <td data-sort="1614380400" id="table_list_tournaments_0_2" class="sorting_1">'
                       '          <a href="media/icals/1655.ics">'
                       '            24.07.2021'
                       '          </a>'
                       '        </td>'
                       '        <td data-sort="1614380400" id="table_list_tournaments_0_3" class="sorting_2">'
                       '          <a href="media/icals/1655.ics">'
                       '            24.07.2021'
                       '          </a>'
                       '        </td>'
                       '        <td data-sort="0" id="table_list_tournaments_0_4">'
                       '          17.03.2021 00:55'
                       '        </td>'
                       '        <td data-sort="1614407326" id="table_list_tournaments_0_5">'
                       '          17.03.2021 00:55'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_6">'
                       '          <span class="badge badge-secondary">'
                       '            Einzelturnier'
                       '          </span>'
                       '        </td>'
                       '        <td class="d-none d-sm-table-cell" id="table_list_tournaments_0_7">'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_8">'
                       '          <!--  Not Logged in: nothing to show here -->'
                       '        </td>'
                       '      </tr>'
                       '      <tr class="even">'
                       '        <td data-sort="Test Tournament #4" id="table_list_tournaments_0_0">'
                       '          <a class="text-muted font-italic"'
                       '            href="https://turniere.discgolf.de/index.php?p=events&amp;sp=view&amp;id=444">'
                       '            Test Tournament #4'
                       '          </a>'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_1">'
                       '          Dortmund'
                       '        </td>'
                       '        <td data-sort="1614380400" id="table_list_tournaments_0_2" class="sorting_1">'
                       '          <a href="media/icals/1655.ics">'
                       '            24.07.2021'
                       '          </a>'
                       '        </td>'
                       '        <td data-sort="1614380400" id="table_list_tournaments_0_3" class="sorting_2">'
                       '          <a href="media/icals/1655.ics">'
                       '            25.07.2021'
                       '          </a>'
                       '        </td>'
                       '        <td data-sort="0" id="table_list_tournaments_0_4">'
                       '          17.03.2021 00:55'
                       '        </td>'
                       '        <td data-sort="1614407326" id="table_list_tournaments_0_5">'
                       '          17.03.2021 00:55'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_6">'
                       '          <span class="badge badge-secondary">'
                       '            Einzelturnier'
                       '          </span>'
                       '        </td>'
                       '        <td class="d-none d-sm-table-cell" id="table_list_tournaments_0_7">'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_8">'
                       '          <!--  Not Logged in: nothing to show here -->'
                       '        </td>'
                       '      </tr>'
                       '    </tbody>'
                       '  </table>'
                       '</body>',
                  status=200)


def add_tournament_list_with_canceled_event():
    responses.add(responses.GET, GT_LIST_PAGE,
                  body='<body>'
                       '  <table class="table table-sm table-striped dataTable no-footer"'
                       '         id="list_tournaments" role="grid"'
                       '         aria-describedby="list_tournaments_info">'
                       '    <thead></thead>'
                       '    <tbody>'
                       '      <tr class="odd">'
                       '        <td data-sort="Test Tournament #5" id="table_list_tournaments_0_0">'
                       '          <h6 style="display:inline;">'
                       '            <span class="badge badge-danger">'
                       '              ABGESAGT'
                       '            </span>'
                       '          </h6>'
                       '          <a class="text-muted font-italic"'
                       '            href="https://turniere.discgolf.de/index.php?p=events&amp;sp=view&amp;id=555">'
                       '            Test Tournament #5'
                       '          </a>'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_1">'
                       '          Dortmund'
                       '        </td>'
                       '        <td data-sort="1614380400" id="table_list_tournaments_0_2" class="sorting_1">'
                       '          <a href="media/icals/1655.ics">'
                       '            24.07.2021'
                       '          </a>'
                       '        </td>'
                       '        <td data-sort="1614380400" id="table_list_tournaments_0_3" class="sorting_2">'
                       '          <a href="media/icals/1655.ics">'
                       '            24.07.2021'
                       '          </a>'
                       '        </td>'
                       '        <td data-sort="0" id="table_list_tournaments_0_4">'
                       '          17.03.2021 00:55'
                       '        </td>'
                       '        <td data-sort="1614407326" id="table_list_tournaments_0_5">'
                       '          17.03.2021 00:55'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_6">'
                       '          <span class="badge badge-secondary">'
                       '            Einzelturnier'
                       '          </span>'
                       '        </td>'
                       '        <td class="d-none d-sm-table-cell" id="table_list_tournaments_0_7">'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_8">'
                       '          <!--  Not Logged in: nothing to show here -->'
                       '        </td>'
                       '      </tr>'
                       '      <tr class="even">'
                       '        <td data-sort="Test Tournament #6" id="table_list_tournaments_0_0">'
                       '          <h6 style="display:inline;">'
                       '            <span class="badge badge-warning">'
                       '              Vorläufig'
                       '            </span>'
                       '          </h6>'
                       '          <a class="text-muted font-italic"'
                       '            href="https://turniere.discgolf.de/index.php?p=events&amp;sp=view&amp;id=666">'
                       '            Test Tournament #6'
                       '          </a>'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_1">'
                       '          Dortmund'
                       '        </td>'
                       '        <td data-sort="1614380400" id="table_list_tournaments_0_2" class="sorting_1">'
                       '          <a href="media/icals/1655.ics">'
                       '            25.07.2021'
                       '          </a>'
                       '        </td>'
                       '        <td data-sort="1614380400" id="table_list_tournaments_0_3" class="sorting_2">'
                       '          <a href="media/icals/1655.ics">'
                       '            25.07.2021'
                       '          </a>'
                       '        </td>'
                       '        <td data-sort="0" id="table_list_tournaments_0_4">'
                       '          17.03.2021 00:55'
                       '        </td>'
                       '        <td data-sort="1614407326" id="table_list_tournaments_0_5">'
                       '          17.03.2021 00:55'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_6">'
                       '          <span class="badge badge-secondary">'
                       '            Einzelturnier'
                       '          </span>'
                       '        </td>'
                       '        <td class="d-none d-sm-table-cell" id="table_list_tournaments_0_7">'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_8">'
                       '          <!--  Not Logged in: nothing to show here -->'
                       '        </td>'
                       '      </tr>'
                       '    </tbody>'
                       '  </table>'
                       '</body>',
                  status=200)


def add_tournament_with_empty_attendance_list(tournament_id):
    responses.add(responses.GET, GT_ATTENDANCE_PAGE.format(tournament_id),
                  body='<body>'
                       '  <table id="starterlist"'
                       '         class="table table-striped table-sm table-hover p-0 m-0 dataTable no-footer"'
                       '         style="font-size: 12px; " role="grid" aria-describedby="starterlist_info">'
                       '    <thead>'
                       '        <tr>'
                       '            <th>Division</th>'
                       '            <th>D-Rating</th>'
                       '            <th>Spieler</th>'
                       '            <th>Wildcards </th>'
                       '            <th>Land</th>'
                       '            <th>GT#</th>'
                       '            <th>PDGA#</th>'
                       '            <th>Angemeldet</th>'
                       '            <th>Status</th>'
                       '        </tr>'
                       '    </thead>'
                       '    <tbody>'
                       '      <tr class="p-0 m-0 odd">'
                       '        <td class="p-0 m-0" id="table_starterlist_0_0">'
                       '          <i>Wildcard</i>'
                       '        </td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_1"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_2"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_3"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_4"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_5"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_6"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_7"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_8"></td>'
                       '      </tr>'
                       '      <tr class="p-0 m-0 even">'
                       '        <td class="p-0 m-0" id="table_starterlist_1_0">'
                       '          <i>Wildcard</i>'
                       '        </td>'
                       '        <td class="p-0 m-0" id="table_starterlist_1_1"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_1_2"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_1_3"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_1_4"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_1_5"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_1_6"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_1_7"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_1_8"></td>'
                       '      </tr>'
                       '    </tbody>'
                       '  </table>'
                       '</body>',
                  status=200)


def add_tournament_without_attendance_list(tournament_id):
    responses.add(responses.GET, GT_ATTENDANCE_PAGE.format(tournament_id),
                  body='<body>'
                       '  <table id="starterlist"'
                       '         class="table table-striped table-sm table-hover p-0 m-0 dataTable no-footer"'
                       '         style="font-size: 12px; " role="grid" aria-describedby="starterlist_info">'
                       '    <thead>'
                       '        <tr>'
                       '            <th>Division</th>'
                       '            <th>D-Rating</th>'
                       '            <th>Spieler</th>'
                       '            <th>Wildcards </th>'
                       '            <th>Land</th>'
                       '            <th>GT#</th>'
                       '            <th>PDGA#</th>'
                       '            <th>Angemeldet</th>'
                       '            <th>Status</th>'
                       '        </tr>'
                       '    </thead>'
                       '    <tbody>'
                       '      <tr class="odd">'
                       '        <td valign="top" colspan="9" class="dataTables_empty">'
                       '          Keine Daten in der Tabelle vorhanden'
                       '        </td>'
                       '      </tr>'
                       '    </tbody>'
                       '  </table>'
                       '</body>',
                  status=200)


def add_tournament_attendance_list(tournament_id):
    responses.add(responses.GET, GT_ATTENDANCE_PAGE.format(tournament_id),
                  body='<body>'
                       '  <table id="starterlist"'
                       '         class="table table-striped table-sm table-hover p-0 m-0 dataTable no-footer"'
                       '         style="font-size: 12px; " role="grid" aria-describedby="starterlist_info">'
                       '    <thead>'
                       '        <tr>'
                       '            <th>Division</th>'
                       '            <th>D-Rating</th>'
                       '            <th>Spieler</th>'
                       '            <th>Wildcards </th>'
                       '            <th>Land</th>'
                       '            <th>GT#</th>'
                       '            <th>PDGA#</th>'
                       '            <th>Angemeldet</th>'
                       '            <th>Status</th>'
                       '        </tr>'
                       '    </thead>'
                       '    <tbody>'
                       '      <tr class="p-0 m-0 odd">'
                       '        <td class="p-0 m-0" id="table_starterlist_0_0">Open</td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_1">	897</td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_2">García García, Manuel</td>'
                       '        <td class="p-0 m-0" data-order="1" id="table_starterlist_0_3">'
                       '          <small><i>(Wildcard)</i></small>'
                       '        </td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_4">DE</td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_5">1922</td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_6"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_7">17.03.2021 01:28</td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_8">bezahlt</td>'
                       '      </tr>'
                       '      <tr class="p-0 m-0 even">'
                       '        <td class="p-0 m-0" id="table_starterlist_1_0">Open</td>'
                       '        <td class="p-0 m-0" id="table_starterlist_1_1">921</td>'
                       '        <td class="p-0 m-0" id="table_starterlist_1_2">Sörenson Sanchez, Federico José</td>'
                       '        <td class="p-0 m-0" data-order="1" id="table_starterlist_1_3">'
                       '          <small><i>(Wildcard)</i></small>'
                       '        </td>'
                       '        <td class="p-0 m-0" id="table_starterlist_1_4">DE</td>'
                       '        <td class="p-0 m-0" id="table_starterlist_1_5">2106</td>'
                       '        <td class="p-0 m-0" id="table_starterlist_1_6">65475</td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_7">17.03.2021 01:29</td>'
                       '        <td class="p-0 m-0" id="table_starterlist_1_8">bezahlt</td>'
                       '      </tr>'
                       '      <tr class="p-0 m-0 odd">'
                       '        <td class="p-0 m-0" id="table_starterlist_44_0">'
                       '          <i>Wildcard</i>'
                       '        </td>'
                       '        <td class="p-0 m-0" id="table_starterlist_44_1"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_44_2"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_44_3"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_44_4"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_44_5"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_44_6"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_44_7"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_44_8"></td>'
                       '      </tr>'
                       '    </tbody>'
                       '  </table>'
                       '</body>',
                  status=200)


def add_tournament_attendance_list_with_other_format(tournament_id):
    responses.add(responses.GET, GT_ATTENDANCE_PAGE.format(tournament_id),
                  body='<body>'
                       '  <table id="starterlist"'
                       '         class="table table-striped table-sm table-hover p-0 m-0 dataTable no-footer"'
                       '         style="font-size: 12px; " role="grid" aria-describedby="starterlist_info">'
                       '    <thead>'
                       '        <tr>'
                       '            <th>Division</th>'
                       '            <th>Aufr.P</th>'
                       '            <th>D-Rating</th>'
                       '            <th>Spieler</th>'
                       '            <th>Wildcards </th>'
                       '            <th>Land</th>'
                       '            <th>GT#</th>'
                       '            <th>PDGA#</th>'
                       '            <th>Angemeldet</th>'
                       '            <th>Status</th>'
                       '        </tr>'
                       '    </thead>'
                       '    <tbody>'
                       '      <tr class="p-0 m-0 odd">'
                       '        <td class="p-0 m-0" id="table_starterlist_0_0">Open</td>'
                       '        <td class="p-0 m-0 sorting_1" id="table_starterlist_0_1">0</td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_2">	897</td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_3">García García, Manuel</td>'
                       '        <td class="p-0 m-0" data-order="1" id="table_starterlist_0_4">'
                       '          <small><i>(Wildcard)</i></small>'
                       '        </td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_5">DE</td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_6">1922</td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_7"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_8">17.03.2021 01:28</td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_9">bezahlt</td>'
                       '      </tr>'
                       '      <tr class="p-0 m-0 even">'
                       '        <td class="p-0 m-0" id="table_starterlist_1_0">Open</td>'
                       '        <td class="p-0 m-0 sorting_1" id="table_starterlist_1_1">0</td>'
                       '        <td class="p-0 m-0" id="table_starterlist_1_2">921</td>'
                       '        <td class="p-0 m-0" id="table_starterlist_1_3">Sörenson Sanchez, Federico</td>'
                       '        <td class="p-0 m-0" data-order="1" id="table_starterlist_1_4">'
                       '          <small><i>(Wildcard)</i></small>'
                       '        </td>'
                       '        <td class="p-0 m-0" id="table_starterlist_1_5">DE</td>'
                       '        <td class="p-0 m-0" id="table_starterlist_1_6">2106</td>'
                       '        <td class="p-0 m-0" id="table_starterlist_1_7">65475</td>'
                       '        <td class="p-0 m-0" id="table_starterlist_0_8">17.03.2021 01:29</td>'
                       '        <td class="p-0 m-0" id="table_starterlist_1_9">bezahlt</td>'
                       '      </tr>'
                       '      <tr class="p-0 m-0 odd">'
                       '        <td class="p-0 m-0" id="table_starterlist_44_0">'
                       '          <i>Wildcard</i>'
                       '        </td>'
                       '        <td class="p-0 m-0" id="table_starterlist_44_1"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_44_2"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_44_3"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_44_4"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_44_5"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_44_6"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_44_7"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_44_8"></td>'
                       '        <td class="p-0 m-0" id="table_starterlist_44_9"></td>'
                       '      </tr>'
                       '    </tbody>'
                       '  </table>'
                       '</body>',
                  status=200)


def add_tournament_list_with_tremonia_series_event():
    responses.add(responses.GET, GT_LIST_PAGE,
                  body='<body>'
                       '  <table class="table table-sm table-striped dataTable no-footer"'
                       '         id="list_tournaments" role="grid"'
                       '         aria-describedby="list_tournaments_info">'
                       '    <thead></thead>'
                       '    <tbody>'
                       '      <tr class="odd">'
                       '        <td data-sort="Test Tournament #5" id="table_list_tournaments_0_0">'
                       '          <h6 style="display:inline;">'
                       '            <span class="badge badge-warning">'
                       '              Vorläufig'
                       '            </span>'
                       '          </h6>'
                       '          <a class="text-muted font-italic"'
                       '            href="https://turniere.discgolf.de/index.php?p=events&amp;sp=view&amp;id=555">'
                       '            Tremonia Series #5'
                       '          </a>'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_1">'
                       '          Dortmund'
                       '        </td>'
                       '        <td data-sort="1614380400" id="table_list_tournaments_0_2" class="sorting_1">'
                       '          <a href="media/icals/1655.ics">'
                       '            24.07.2021'
                       '          </a>'
                       '        </td>'
                       '        <td data-sort="1614380400" id="table_list_tournaments_0_3" class="sorting_2">'
                       '          <a href="media/icals/1655.ics">'
                       '            24.07.2021'
                       '          </a>'
                       '        </td>'
                       '        <td data-sort="0" id="table_list_tournaments_0_4">'
                       '          17.03.2021 00:55'
                       '        </td>'
                       '        <td data-sort="1614407326" id="table_list_tournaments_0_5">'
                       '          17.03.2021 00:55'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_6">'
                       '          <span class="badge badge-secondary">'
                       '            Einzelturnier'
                       '          </span>'
                       '        </td>'
                       '        <td class="d-none d-sm-table-cell" id="table_list_tournaments_0_7">'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_8">'
                       '          <!--  Not Logged in: nothing to show here -->'
                       '        </td>'
                       '      </tr>'
                       '      <tr class="even">'
                       '        <td data-sort="Test Tournament #6" id="table_list_tournaments_0_0">'
                       '          <h6 style="display:inline;">'
                       '            <span class="badge badge-warning">'
                       '              Vorläufig'
                       '            </span>'
                       '          </h6>'
                       '          <a class="text-muted font-italic"'
                       '            href="https://turniere.discgolf.de/index.php?p=events&amp;sp=view&amp;id=666">'
                       '            Tremonia Series #6'
                       '          </a>'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_1">'
                       '          Dortmund'
                       '        </td>'
                       '        <td data-sort="1614380400" id="table_list_tournaments_0_2" class="sorting_1">'
                       '          <a href="media/icals/1655.ics">'
                       '            25.07.2021'
                       '          </a>'
                       '        </td>'
                       '        <td data-sort="1614380400" id="table_list_tournaments_0_3" class="sorting_2">'
                       '          <a href="media/icals/1655.ics">'
                       '            25.07.2021'
                       '          </a>'
                       '        </td>'
                       '        <td data-sort="0" id="table_list_tournaments_0_4">'
                       '          17.03.2021 00:55'
                       '        </td>'
                       '        <td data-sort="1614407326" id="table_list_tournaments_0_5">'
                       '          17.03.2021 00:55'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_6">'
                       '          <span class="badge badge-secondary">'
                       '            Einzelturnier'
                       '          </span>'
                       '        </td>'
                       '        <td class="d-none d-sm-table-cell" id="table_list_tournaments_0_7">'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_8">'
                       '          <!--  Not Logged in: nothing to show here -->'
                       '        </td>'
                       '      </tr>'
                       '    </tbody>'
                       '  </table>'
                       '</body>',
                  status=200)


def add_tournament_list_with_pdga_event():
    responses.add(responses.GET, GT_LIST_PAGE,
                  body='<body>'
                       '  <table class="table table-sm table-striped dataTable no-footer"'
                       '         id="list_tournaments" role="grid"'
                       '         aria-describedby="list_tournaments_info">'
                       '    <thead></thead>'
                       '    <tbody>'
                       '      <tr class="odd">'
                       '        <td data-sort="Tremonia Open" id="table_list_tournaments_0_0">'
                       '          <h6 style="display:inline;">'
                       '            <span class="badge badge-warning">'
                       '              Vorläufig'
                       '            </span>'
                       '          </h6>'
                       '          <a class="text-muted font-italic"'
                       '            href="https://turniere.discgolf.de/index.php?p=events&amp;sp=view&amp;id=777">'
                       '            Tremonia Open'
                       '          </a>'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_1">'
                       '          Dortmund'
                       '        </td>'
                       '        <td data-sort="1614380400" id="table_list_tournaments_0_2" class="sorting_1">'
                       '          <a href="media/icals/1655.ics">'
                       '            24.07.2021'
                       '          </a>'
                       '        </td>'
                       '        <td data-sort="1614380400" id="table_list_tournaments_0_3" class="sorting_2">'
                       '          <a href="media/icals/1655.ics">'
                       '            25.07.2021'
                       '          </a>'
                       '        </td>'
                       '        <td data-sort="0" id="table_list_tournaments_0_4">'
                       '          17.03.2021 00:55'
                       '        </td>'
                       '        <td data-sort="1614407326" id="table_list_tournaments_0_5">'
                       '          17.03.2021 00:55'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_6">'
                       '          <span class="badge badge-secondary">'
                       '            Einzelturnier'
                       '          </span>'
                       '        </td>'
                       '        <td class="d-none d-sm-table-cell" id="table_list_tournaments_0_7">'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_8">'
                       '          <!--  Not Logged in: nothing to show here -->'
                       '        </td>'
                       '      </tr>'
                       '      <tr class="even">'
                       '        <td data-sort="Tremonia Classics" id="table_list_tournaments_0_0">'
                       '          <h6 style="display:inline;">'
                       '            <span class="badge badge-warning">'
                       '              Vorläufig'
                       '            </span>'
                       '          </h6>'
                       '          <a class="text-muted font-italic"'
                       '            href="https://turniere.discgolf.de/index.php?p=events&amp;sp=view&amp;id=888">'
                       '            Tremonia Classics'
                       '          </a>'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_1">'
                       '          Dortmund'
                       '        </td>'
                       '        <td data-sort="1614380400" id="table_list_tournaments_0_2" class="sorting_1">'
                       '          <a href="media/icals/1655.ics">'
                       '            26.07.2021'
                       '          </a>'
                       '        </td>'
                       '        <td data-sort="1614380400" id="table_list_tournaments_0_3" class="sorting_2">'
                       '          <a href="media/icals/1655.ics">'
                       '            27.07.2021'
                       '          </a>'
                       '        </td>'
                       '        <td data-sort="0" id="table_list_tournaments_0_4">'
                       '          17.03.2021 00:55'
                       '        </td>'
                       '        <td data-sort="1614407326" id="table_list_tournaments_0_5">'
                       '          17.03.2021 00:55'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_6">'
                       '          <span class="badge badge-secondary">'
                       '            Einzelturnier'
                       '          </span>'
                       '        </td>'
                       '        <td class="d-none d-sm-table-cell" id="table_list_tournaments_0_7">'
                       '        </td>'
                       '        <td id="table_list_tournaments_0_8">'
                       '          <!--  Not Logged in: nothing to show here -->'
                       '        </td>'
                       '      </tr>'
                       '    </tbody>'
                       '  </table>'
                       '</body>',
                  status=200)
