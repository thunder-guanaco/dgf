from datetime import date

import responses
from django.test import TestCase

from dgf import german_tour
from dgf.german_tour.common import ColumnNotFound
from dgf.models import Friend, Division, Result, Tournament
from dgf_cms.settings import GT_RATINGS_PAGE, GT_RESULTS_PAGE, GT_DETAILS_PAGE

JULY_24 = date(year=2021, month=7, day=24)
JULY_25 = date(year=2021, month=7, day=25)
JULY_26 = date(year=2021, month=7, day=26)


class GermanTourResultsTest(TestCase):

    def setUp(self):
        Friend.objects.all().delete()
        Result.objects.all().delete()
        Tournament.objects.all().delete()

    @responses.activate
    def test_tournament_results(self):

        mpo, _ = Division.objects.get_or_create(id='MPO')
        manolo = Friend.objects.create(username='manolo', first_name='Manolo', gt_number=1922)
        fede = Friend.objects.create(username='fede', first_name='Fede', gt_number=2106)

        add_rating_page(1922, [333])
        add_rating_page(2106, [333, 444])
        add_tournament_results(333,
                               'Test Tournament #3',
                               '24.07.2021 - 25.07.2021',
                               ([1, 2, 1922, 4, 5, 2106], []))
        add_tournament_results(444,
                               'Test Tournament #4',
                               '26.07.2021',
                               ([2106, 2, 3], [1922]))

        german_tour.update_all_tournaments_results()

        manolo_results = Result.objects.filter(friend=manolo)
        self.assertEqual(len(manolo_results), 1)

        result_tournament_3 = manolo_results.get(tournament__gt_id=333)
        self.assertEqual(result_tournament_3.position, 3)
        self.assertEqual(result_tournament_3.division, mpo)
        self.assertEqual(result_tournament_3.tournament.gt_id, 333)
        self.assertEqual(result_tournament_3.tournament.name, 'Test Tournament #3')
        self.assertEqual(result_tournament_3.tournament.url,
                         'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=333')
        self.assertEqual(result_tournament_3.tournament.begin, JULY_24)
        self.assertEqual(result_tournament_3.tournament.end, JULY_25)

        fede_results = Result.objects.filter(friend=fede)
        self.assertEqual(len(fede_results), 2)

        result_tournament_3 = fede_results.get(tournament__gt_id=333)
        self.assertEqual(result_tournament_3.position, 6)
        self.assertEqual(result_tournament_3.division, mpo)
        self.assertEqual(result_tournament_3.tournament.gt_id, 333)
        self.assertEqual(result_tournament_3.tournament.name, 'Test Tournament #3')
        self.assertEqual(result_tournament_3.tournament.url,
                         'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=333')
        self.assertEqual(result_tournament_3.tournament.begin, JULY_24)
        self.assertEqual(result_tournament_3.tournament.end, JULY_25)

        result_tournament_4 = fede_results.get(tournament__gt_id=444)
        self.assertEqual(result_tournament_4.position, 1)
        self.assertEqual(result_tournament_4.division, mpo)
        self.assertEqual(result_tournament_4.tournament.gt_id, 444)
        self.assertEqual(result_tournament_4.tournament.name, 'Test Tournament #4')
        self.assertEqual(result_tournament_4.tournament.url,
                         'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=444')
        self.assertEqual(result_tournament_4.tournament.begin, JULY_26)
        self.assertEqual(result_tournament_4.tournament.end, JULY_26)

    @responses.activate
    def test_tournament_results_with_broken_page(self):
        Friend.objects.create(username='manolo', first_name='Manolo', gt_number=1922)
        add_rating_page(1922, [333])
        add_broken_tournament_results(333,
                                      'Test Tournament #3',
                                      '24.07.2021 - 25.07.2021',
                                      ([1, 2, 1922, 4, 5, 2106], []))

        try:
            german_tour.update_all_tournaments_results()
            self.fail('This should have thrown an exception')
        except ColumnNotFound as error:
            self.assertEqual(error.text, 'Division ')

    @responses.activate
    def test_results_from_one_tournament(self):
        mpo, _ = Division.objects.get_or_create(id='MPO')
        manolo = Friend.objects.create(username='manolo', first_name='Manolo', gt_number=1922)
        tournament = Tournament.objects.create(gt_id=333, name='Test Tournament #3', begin=JULY_24, end=JULY_25)
        add_tournament_results(333,
                               'Test Tournament #3',
                               '24.07.2021 - 25.07.2021',
                               ([1, 2, 1922], []))

        german_tour.update_tournament_results(tournament)

        manolo_results = Result.objects.filter(friend=manolo)
        self.assertEqual(len(manolo_results), 1)
        result_tournament_3 = manolo_results.get(tournament__gt_id=333)
        self.assertEqual(result_tournament_3.position, 3)
        self.assertEqual(result_tournament_3.division, mpo)
        self.assertEqual(result_tournament_3.tournament.gt_id, 333)
        self.assertEqual(result_tournament_3.tournament.name, 'Test Tournament #3')
        self.assertEqual(result_tournament_3.tournament.url,
                         'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=333')
        self.assertEqual(result_tournament_3.tournament.begin, JULY_24)
        self.assertEqual(result_tournament_3.tournament.end, JULY_25)


def add_rating_page(player_gt_id, tournament_gt_ids):
    body = '<body>'
    for gt_id in tournament_gt_ids:
        body += ('  <td style="">'
                 '    <a title="GT Ergebnisse"'
                 '     target="_blank"'
                 f'     href="https://turniere.discgolf.de/index.php?p=events&amp;sp=list-results&amp;id={gt_id}">'
                 '      GT Ergebnisse'
                 '    </a>'
                 '  </td>'
                 )
    body += '</body>'
    responses.add(responses.GET, GT_RATINGS_PAGE.format(player_gt_id), body=body, status=200)


def add_tournament_results(tournament_id, tournament_name, date, gt_ids):
    responses.add(responses.GET, GT_DETAILS_PAGE.format(tournament_id),
                  body='<body>'
                       f'  <h2>{tournament_name}</h2>'
                       '  <table class="tabletable-sm">'
                       '    <tbody>'
                       '      <tr>'
                       '        <td>Ansprechpartner/Turnierdirektor</td>'
                       '        <td>DRIVEDiscGolf(DavidStrott)</td>'
                       '      </tr>'
                       '      <tr>'
                       '        <td>Ort</td>'
                       '        <td>'
                       '          <a href="http://www.google.com/maps/place/51.517945,7.398306" target="_blank">'
                       '            Dortmund'
                       '          </a>'
                       '        </td>'
                       '      </tr>'
                       '      <tr>'
                       '        <td>Turnierbetrieb</td>'
                       f'       <td>{date}</td>'
                       '      </tr>'
                       '      <tr>'
                       '        <td>PDGAStatus</td>'
                       '        <td>'
                       '          <a href="https://www.pdga.com/tour/event/57760"target="_blank">C-Tier</a>'
                       '        </td>'
                       '      </tr>    '
                       '    </tbody>'
                       '  </table>'
                       '</body>',
                  status=200)

    body = '<body>\n'
    body += ('  <table class="table table-striped table-sm" style="font-size: 12px; " id="results_layout_">'
             '    <thead>'
             '      <tr>'
             '        <th>Division </th>'
             '        <th>#</th>'
             '        <th>Name</th>'
             '        <th>f.Div</th>'
             '        <th>GT#</th>'
             '        <th>par</th>'
             '        <th>R1</th>'
             '        <th>R2</th>'
             '        <th>Gesamt</th>'
             '        <th>Kommentar</th>'
             '      </tr>'
             '    </thead>'
             '    <tbody>')
    # gt_ids[0] contains the sorted results
    for position, gt_id in enumerate(gt_ids[0], start=1):
        body += ('    <tr style="line-height: 10px; min-height: 10px; height: 10px;" class="">'
                 '        <td>O</td>'
                 f'       <td class="text-right" data-order="{position}">{position}</td>'
                 '        <td>Name, Vorname</td>'
                 '        <td></td>'
                 f'       <td>{gt_id}</td>'
                 '        <td>-18</td>'
                 '        <td>49</td>'
                 '        <td>45</td>'
                 '        <td data-order="94">94</td>'
                 '        <td></td>'
                 '      </tr>')
    # gt_ids[1] contains the DNFs
    for gt_id in gt_ids[1]:
        body += ('    <tr style="line-height: 10px; min-height: 10px; height: 10px;" class="">'
                 '        <td>O</td>'
                 f'       <td class="text-right" data-order="9999"> DNF </td>'
                 '        <td>Name, Vorname</td>'
                 '        <td></td>'
                 f'       <td>{gt_id}</td>'
                 '        <td>-</td>'
                 '        <td>49</td>'
                 '        <td>999</td>'
                 '        <td data-order="9999"> DNF </td>'
                 '        <td></td>'
                 '      </tr>')
    body += ('    </tbody>'
             '  </table>'
             '</body>')
    responses.add(responses.GET, GT_RESULTS_PAGE.format(tournament_id), body=body, status=200)


def add_broken_tournament_results(tournament_id, tournament_name, date, gt_ids):
    responses.add(responses.GET, GT_DETAILS_PAGE.format(tournament_id),
                  body='<body>'
                       f'  <h2>{tournament_name}</h2>'
                       '  <table class="tabletable-sm">'
                       '    <tbody>'
                       '      <tr>'
                       '        <td>Ansprechpartner/Turnierdirektor</td>'
                       '        <td>DRIVEDiscGolf(DavidStrott)</td>'
                       '      </tr>'
                       '      <tr>'
                       '        <td>Ort</td>'
                       '        <td>'
                       '          <a href="http://www.google.com/maps/place/51.517945,7.398306" target="_blank">'
                       '            Dortmund'
                       '          </a>'
                       '        </td>'
                       '      </tr>'
                       '      <tr>'
                       '        <td>Turnierbetrieb</td>'
                       f'       <td>{date}</td>'
                       '      </tr>'
                       '      <tr>'
                       '        <td>PDGAStatus</td>'
                       '        <td>'
                       '          <a href="https://www.pdga.com/tour/event/57760"target="_blank">C-Tier</a>'
                       '        </td>'
                       '      </tr>    '
                       '    </tbody>'
                       '  </table>'
                       '</body>',
                  status=200)

    body = '<body>\n'
    body += ('  <table class="table table-striped table-sm" style="font-size: 12px; " id="results_layout_">'
             '    <thead>'
             '      <tr>'
             '        <th>#</th>'
             '        <th>Name</th>'
             '        <th>f.Div</th>'
             '        <th>GT#</th>'
             '        <th>par</th>'
             '        <th>R1</th>'
             '        <th>R2</th>'
             '        <th>Gesamt</th>'
             '        <th>Kommentar</th>'
             '      </tr>'
             '    </thead>'
             '    <tbody>')
    # gt_ids[0] contains the sorted results
    for position, gt_id in enumerate(gt_ids[0], start=1):
        body += ('    <tr style="line-height: 10px; min-height: 10px; height: 10px;" class="">'
                 '        <td>O</td>'
                 f'       <td class="text-right" data-order="{position}">{position}</td>'
                 '        <td>Name, Vorname</td>'
                 '        <td></td>'
                 f'       <td>{gt_id}</td>'
                 '        <td>-18</td>'
                 '        <td>49</td>'
                 '        <td>45</td>'
                 '        <td data-order="94">94</td>'
                 '        <td></td>'
                 '      </tr>')
    # gt_ids[1] contains the DNFs
    for gt_id in gt_ids[1]:
        body += ('    <tr style="line-height: 10px; min-height: 10px; height: 10px;" class="">'
                 '        <td>O</td>'
                 f'       <td class="text-right" data-order="9999"> DNF </td>'
                 '        <td>Name, Vorname</td>'
                 '        <td></td>'
                 f'       <td>{gt_id}</td>'
                 '        <td>-</td>'
                 '        <td>49</td>'
                 '        <td>999</td>'
                 '        <td data-order="9999"> DNF </td>'
                 '        <td></td>'
                 '      </tr>')
    body += ('    </tbody>'
             '  </table>'
             '</body>')
    responses.add(responses.GET, GT_RESULTS_PAGE.format(tournament_id), body=body, status=200)
