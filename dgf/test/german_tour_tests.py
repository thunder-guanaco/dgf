from datetime import date

import responses
from django.test import TestCase

from dgf import german_tour
from dgf.german_tour import TOURNAMENT_LIST_PAGE, TOURNAMENT_ATTENDANCE_PAGE
from dgf.models import Tournament, Friend, Attendance

APRIL_2 = date(year=2021, month=4, day=2)
JULY_24 = date(year=2021, month=7, day=24)
JULY_25 = date(year=2021, month=7, day=25)


class GermanTourTest(TestCase):

    @responses.activate
    def test_tournament_without_attendance_and_with_empty_attendance(self):
        self.add_tournament_list()
        self.add_tournament_without_attendance_list(333)
        self.add_tournament_with_empty_attendance_list(444)
        Friend.objects.create(username='manolo', gt_number=1922)

        german_tour.update_tournaments()

        attendance_list = list(Attendance.objects.all())
        self.assertListEqual(attendance_list, [])

    @responses.activate
    def test_tournament_without_attendance_and_with_empty_attendance_existing_tournaments(self):
        self.add_tournament_list()
        self.add_tournament_with_empty_attendance_list(333)
        self.add_tournament_without_attendance_list(444)
        Tournament.objects.create(gt_id=333, name='Tremonia Series #3', begin=JULY_24, end=JULY_24)
        Tournament.objects.create(gt_id=444, name='Tremonia Series #4', begin=JULY_24, end=JULY_25)
        Friend.objects.create(username='manolo', gt_number=1922)

        german_tour.update_tournaments()

        attendance_list = list(Attendance.objects.all())
        self.assertListEqual(attendance_list, [])

    @responses.activate
    def test_tournament_with_attendance_no_tournaments(self):
        self.add_tournament_list()
        self.add_tournament_attendance_list(333)
        self.add_tournament_attendance_list(444)
        manolo = Friend.objects.create(username='manolo', gt_number=1922)

        german_tour.update_tournaments()

        attendance_list = Attendance.objects.filter(friend=manolo)
        self.assertEqual(len(attendance_list), 2)

        attendance_ts3 = attendance_list.get(tournament__gt_id=333)
        self.assertEqual(attendance_ts3.tournament.name, 'Tremonia Series #3')
        self.assertEqual(attendance_ts3.tournament.begin, JULY_24)
        self.assertEqual(attendance_ts3.tournament.end, JULY_24)
        self.assertEqual(attendance_ts3.friend, manolo)

        attendance_ts4 = attendance_list.get(tournament__gt_id=444)
        self.assertEqual(attendance_ts4.tournament.name, 'Tremonia Series #4')
        self.assertEqual(attendance_ts4.tournament.begin, JULY_24)
        self.assertEqual(attendance_ts4.tournament.end, JULY_25)
        self.assertEqual(attendance_ts4.friend, manolo)

    @responses.activate
    def test_tournament_with_attendance_no_tournaments_with_different_attendance_formats(self):
        self.add_tournament_list()
        self.add_tournament_attendance_list(333)
        self.add_tournament_attendance_list_with_other_format(444)
        manolo = Friend.objects.create(username='manolo', gt_number=1922)

        german_tour.update_tournaments()

        attendance_list = Attendance.objects.filter(friend=manolo)
        self.assertEqual(len(attendance_list), 2)

        attendance_ts3 = attendance_list.get(tournament__gt_id=333)
        self.assertEqual(attendance_ts3.tournament.name, 'Tremonia Series #3')
        self.assertEqual(attendance_ts3.tournament.begin, JULY_24)
        self.assertEqual(attendance_ts3.tournament.end, JULY_24)
        self.assertEqual(attendance_ts3.friend, manolo)

        attendance_ts4 = attendance_list.get(tournament__gt_id=444)
        self.assertEqual(attendance_ts4.tournament.name, 'Tremonia Series #4')
        self.assertEqual(attendance_ts4.tournament.begin, JULY_24)
        self.assertEqual(attendance_ts4.tournament.end, JULY_25)
        self.assertEqual(attendance_ts4.friend, manolo)

    @responses.activate
    def test_tournament_with_attendance_existing_tournaments(self):
        self.add_tournament_list()
        self.add_tournament_attendance_list(333)
        self.add_tournament_attendance_list(444)
        manolo = Friend.objects.create(username='manolo', gt_number=1922)
        ts3 = Tournament.objects.create(gt_id=333, name='Tremonia Series #3', begin=JULY_24, end=JULY_24)
        ts4 = Tournament.objects.create(gt_id=444, name='Tremonia Series #4', begin=JULY_24, end=JULY_25)

        german_tour.update_tournaments()

        attendance_list = Attendance.objects.filter(friend=manolo)
        self.assertEqual(len(attendance_list), 2)

        attendance_ts3 = attendance_list.get(tournament__gt_id=333)
        self.assertEqual(attendance_ts3.tournament, ts3)
        self.assertEqual(attendance_ts3.friend, manolo)

        attendance_ts4 = attendance_list.get(tournament__gt_id=444)
        self.assertEqual(attendance_ts4.tournament, ts4)
        self.assertEqual(attendance_ts4.friend, manolo)

    @responses.activate
    def test_tournament_with_attendance_existing_attendance_existing_tournaments(self):
        self.add_tournament_list()
        self.add_tournament_attendance_list(333)
        self.add_tournament_attendance_list(444)
        manolo = Friend.objects.create(username='manolo', gt_number=1922)
        ts3 = Tournament.objects.create(gt_id=333, name='Tremonia Series #3', begin=JULY_24, end=JULY_24)
        ts4 = Tournament.objects.create(gt_id=444, name='Tremonia Series #4', begin=JULY_24, end=JULY_25)
        Attendance.objects.create(friend=manolo, tournament=ts3)
        Attendance.objects.create(friend=manolo, tournament=ts4)

        german_tour.update_tournaments()

        attendance_list = Attendance.objects.filter(friend=manolo)
        self.assertEqual(len(attendance_list), 2)

        attendance_ts3 = attendance_list.get(tournament__gt_id=333)
        self.assertEqual(attendance_ts3.tournament, ts3)
        self.assertEqual(attendance_ts3.friend, manolo)

        attendance_ts4 = attendance_list.get(tournament__gt_id=444)
        self.assertEqual(attendance_ts4.tournament, ts4)
        self.assertEqual(attendance_ts4.friend, manolo)

    @responses.activate
    def test_tournament_date_change(self):
        self.add_tournament_list()
        self.add_tournament_attendance_list(333)
        self.add_tournament_attendance_list(444)

        Tournament.objects.create(gt_id=333, name='Tremonia Series #3', begin=APRIL_2, end=APRIL_2)
        Tournament.objects.create(gt_id=444, name='Tremonia Series #4', begin=JULY_24, end=JULY_24)

        german_tour.update_tournaments()

        ts3 = Tournament.objects.get(gt_id=333)
        self.assertEqual(ts3.begin, JULY_24)
        self.assertEqual(ts3.end, JULY_24)

        ts4 = Tournament.objects.get(gt_id=444)
        self.assertEqual(ts4.begin, JULY_24)
        self.assertEqual(ts4.end, JULY_25)

    @responses.activate
    def test_canceled_tournament_non_existing(self):
        self.add_tournament_list_with_canceled_event()
        self.add_tournament_with_empty_attendance_list(666)

        german_tour.update_tournaments()

        ts5 = list(Tournament.objects.filter(gt_id=555))
        self.assertEqual(ts5, [])

        ts6 = Tournament.objects.get(gt_id=666)
        self.assertEqual(ts6.name, 'Tremonia Series #6')
        self.assertEqual(ts6.begin, JULY_25)
        self.assertEqual(ts6.end, JULY_25)

    @responses.activate
    def test_canceled_tournament_with_existing_tournament_without_attendance(self):
        self.add_tournament_list_with_canceled_event()
        self.add_tournament_with_empty_attendance_list(666)

        Tournament.objects.create(gt_id=555, name='Tremonia Series #5', begin=JULY_24, end=JULY_24)
        Tournament.objects.create(gt_id=666, name='Tremonia Series #6', begin=JULY_25, end=JULY_25)

        german_tour.update_tournaments()

        ts5 = list(Tournament.objects.filter(gt_id=555))
        self.assertEqual(ts5, [])

        ts6 = Tournament.objects.get(gt_id=666)
        self.assertEqual(ts6.name, 'Tremonia Series #6')
        self.assertEqual(ts6.begin, JULY_25)
        self.assertEqual(ts6.end, JULY_25)

    @responses.activate
    def test_canceled_tournament_with_existing_tournament_with_attendance(self):
        self.add_tournament_list_with_canceled_event()
        self.add_tournament_with_empty_attendance_list(666)

        manolo = Friend.objects.create(username='manolo', gt_number=1922)
        ts5 = Tournament.objects.create(gt_id=555, name='Tremonia Series #5', begin=JULY_24, end=JULY_24)
        ts6 = Tournament.objects.create(gt_id=666, name='Tremonia Series #6', begin=JULY_25, end=JULY_25)
        Attendance.objects.create(friend=manolo, tournament=ts5)
        Attendance.objects.create(friend=manolo, tournament=ts6)

        german_tour.update_tournaments()

        ts5 = list(Tournament.objects.filter(gt_id=555))
        self.assertEqual(ts5, [])

        ts6 = Tournament.objects.get(gt_id=666)
        self.assertEqual(ts6.name, 'Tremonia Series #6')
        self.assertEqual(ts6.begin, JULY_25)
        self.assertEqual(ts6.end, JULY_25)

    def add_tournament_list(self):
        responses.add(responses.GET, TOURNAMENT_LIST_PAGE,
                      body='<body>'
                           '  <table class="table table-sm table-striped dataTable no-footer"'
                           '         id="list_tournaments" role="grid"'
                           '         aria-describedby="list_tournaments_info">'
                           '    <thead></thead>'
                           '    <tbody>'
                           '      <tr class="odd">'
                           '        <td data-sort="Tremonia Series #3" id="table_list_tournaments_0_0">'
                           '          <a class="text-muted font-italic"'
                           '            href="https://turniere.discgolf.de/index.php?p=events&amp;sp=view&amp;id=333">'
                           '            Tremonia Series #3'
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
                           '        <td data-sort="Tremonia Series #4" id="table_list_tournaments_0_0">'
                           '          <a class="text-muted font-italic"'
                           '            href="https://turniere.discgolf.de/index.php?p=events&amp;sp=view&amp;id=444">'
                           '            Tremonia Series #4'
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

    def add_tournament_list_with_canceled_event(self):
        responses.add(responses.GET, TOURNAMENT_LIST_PAGE,
                      body='<body>'
                           '  <table class="table table-sm table-striped dataTable no-footer"'
                           '         id="list_tournaments" role="grid"'
                           '         aria-describedby="list_tournaments_info">'
                           '    <thead></thead>'
                           '    <tbody>'
                           '      <tr class="odd">'
                           '        <td data-sort="Tremonia Series #5" id="table_list_tournaments_0_0">'
                           '          <h6 style="display:inline;">'
                           '            <span class="badge badge-danger">'
                           '              ABGESAGT'
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
                           '        <td data-sort="Tremonia Series #6" id="table_list_tournaments_0_0">'
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

    def add_tournament_with_empty_attendance_list(self, tournament_id):
        responses.add(responses.GET, TOURNAMENT_ATTENDANCE_PAGE.format(tournament_id),
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

    def add_tournament_without_attendance_list(self, tournament_id):
        responses.add(responses.GET, TOURNAMENT_ATTENDANCE_PAGE.format(tournament_id),
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

    def add_tournament_attendance_list(self, tournament_id):
        responses.add(responses.GET, TOURNAMENT_ATTENDANCE_PAGE.format(tournament_id),
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

    def add_tournament_attendance_list_with_other_format(self, tournament_id):
        responses.add(responses.GET, TOURNAMENT_ATTENDANCE_PAGE.format(tournament_id),
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
