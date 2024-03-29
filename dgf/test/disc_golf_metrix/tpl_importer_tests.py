from datetime import date

import responses
from django.test import TestCase

from dgf.disc_golf_metrix.tremonia_putting_liga import TremoniaPuttingLigaImporter, WHATEVER
from dgf.models import Tournament, Friend, Tour, Division
from dgf.test.disc_golf_metrix.tpl_responses import add_three_tpl_tournaments, add_one_tpl_tournament, \
    add_three_tpl_tournaments_for_tours
from dgf.test.models.creator import create_divisions
from dgf_cms.settings import DISC_GOLF_METRIX_TOURNAMENT_PAGE


class TremoniaPuttingLigaImportTest(TestCase):
    def setUp(self):
        Tournament.objects.all().delete()
        Tour.objects.all().delete()
        Friend.objects.all().delete()
        Division.objects.all().delete()
        create_divisions()

    @responses.activate
    def test_tournaments(self):
        add_three_tpl_tournaments()

        TremoniaPuttingLigaImporter().update_tournaments()

        tournaments = Tournament.objects.filter(name__endswith='. Spieltag Tremonia Putting Liga')
        self.assertEqual(tournaments.count(), 3)
        for id in [1, 2, 3]:
            self.assert_tournament(tournaments, id)

    @responses.activate
    def test_tournament_with_results(self):
        Friend.objects.create(username='manolo', first_name='Manolo', metrix_user_id='manolo')
        Friend.objects.create(username='fede', first_name='Federico', metrix_user_id='fede')
        add_one_tpl_tournament(12345, '1. Spieltag', '1000-01-01',
                               players=[
                                   ('manolo', 1, 'Open',
                                    [[0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [0, 1, 2, 3, 0], [3, 0, 3, 0, 3]]),
                                   ('dirk', 2, 'Open',
                                    [[3, 3, 3, 3, 3], [2, 2, 2, 2, 2], [1, 1, 1, 1, 1], [0, 0, 0, 0, 0]]),
                               ])

        TremoniaPuttingLigaImporter().update_tournaments()

        tournament = Tournament.objects.get(metrix_id=12345)
        results = [(result.friend.username, result.position, result.division.id, result.points) for result in
                   tournament.results.all().order_by('-points')]
        self.assertEqual(results, [('dirk', WHATEVER, 'MPO', 95), ('manolo', WHATEVER, 'MPO', 66)])

    @responses.activate
    def test_tournament_without_results(self):
        add_one_tpl_tournament(12345, '1. Spieltag', '1000-01-01')

        TremoniaPuttingLigaImporter().update_tournaments()

        tournament = Tournament.objects.get(metrix_id=12345)
        self.assertEqual(tournament.results.all().count(), 0)

    @responses.activate
    def test_add_automatic_tours(self):
        Friend.objects.create(username='manolo', first_name='Manolo', metrix_user_id='manolo')
        Friend.objects.create(username='fede', first_name='Federico', metrix_user_id='fede')
        add_three_tpl_tournaments_for_tours(players=[
            ('manolo', 1, 'Open',
             [[0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [0, 1, 2, 3, 0], [3, 0, 3, 0, 3]]),
        ])

        TremoniaPuttingLigaImporter().update_tournaments()

        self.assert_tournament_in_tour('1. Tremonia Putting Liga', 'MPO', {1, 2}, expected_evaluate_how_many=6)
        # tournament 3 doesn't have any results and therefore there are no divisions, and it won't be added

    @responses.activate
    def test_add_automatic_tours_with_existing_tour(self):
        Friend.objects.create(username='manolo', first_name='Manolo', metrix_user_id='manolo')
        Friend.objects.create(username='fede', first_name='Federico', metrix_user_id='fede')
        mpo, _ = Division.objects.get_or_create(id='MPO')
        Tour.objects.create(name='1. Tremonia Putting Liga',
                            division=mpo,
                            evaluate_how_many=6)
        add_three_tpl_tournaments_for_tours(players=[
            ('manolo', 1, 'Open',
             [[0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [0, 1, 2, 3, 0], [3, 0, 3, 0, 3]]),
        ])

        TremoniaPuttingLigaImporter().update_tournaments()

        self.assert_tournament_in_tour('1. Tremonia Putting Liga', 'MPO', {1, 2}, expected_evaluate_how_many=6)
        # tournament 3 doesn't have any results and therefore there are no divisions, and it won't be added

    def assert_tournament_in_tour(self, name, division, expected_metrix_ids, expected_evaluate_how_many=10000):
        tour = Tour.objects.get(name=name, division=division)
        tournaments = set(tour.tournaments.all().values_list('metrix_id', flat=True))
        self.assertEqual(tour.evaluate_how_many, expected_evaluate_how_many)
        self.assertEqual(tournaments, expected_metrix_ids)

    def assert_tournament(self, tournaments, id):
        tournament = tournaments.get(metrix_id=id)
        self.assertEqual(tournament.name, f'{id}. Spieltag Tremonia Putting Liga')
        self.assertEqual(tournament.url, DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(id))
        self.assertEqual(tournament.begin, date(year=1000 * id, month=1, day=1))
        self.assertEqual(tournament.end, date(year=1000 * id, month=1, day=1))
