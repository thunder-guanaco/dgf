from datetime import date

import responses

from dgf import german_tour
from dgf.german_tour.common import ColumnNotFound
from dgf.models import Friend, Division, Result, Tournament
from dgf.test.german_tour.german_tour_test import GermanTourTest
from dgf.test.german_tour.responses import add_details_page, add_results_page, add_rating_page, add_list_page, \
    add_empty_results_page

PAST_JULY_24 = date(year=2021, month=7, day=24)
PAST_JULY_25 = date(year=2021, month=7, day=25)
PAST_JULY_26 = date(year=2021, month=7, day=26)


class GermanTourResultsTest(GermanTourTest):

    def setUp(self):
        super().setUp()
        Result.objects.all().delete()
        Division.objects.all().delete()

    @responses.activate
    def test_tournament_empty_results(self):
        Division.objects.create(id='MPO')
        Friend.objects.create(username='manolo', gt_number=1922)

        add_list_page([])
        add_rating_page(1922, [333])
        add_details_page(333, 'Test Tournament #3', '24.07.2021 - 25.07.2021')
        add_empty_results_page(333)

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(1)
        self.assert_results_amount(0)

    @responses.activate
    def test_tournament_results_coming_from_list_page(self):
        mpo = Division.objects.create(id='MPO')
        manolo = Friend.objects.create(username='manolo', gt_number=1922)
        fede = Friend.objects.create(username='fede', gt_number=2106)

        add_list_page([333])
        add_rating_page(1922, [])
        add_rating_page(2106, [444])
        add_details_page(333, 'Test Tournament #3', '24.07.2021 - 25.07.2021')
        add_results_page(333, [1, 2, 1922, 4, 5, 2106])
        add_details_page(444, 'Test Tournament #4', '26.07.2021')
        add_results_page(444, [2106, 2, 3], dnf=[1922])

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(2)
        self.assert_results_amount(3)
        self.assert_result(manolo, 333, 3, mpo)
        self.assert_result(fede, 333, 6, mpo)
        self.assert_result(fede, 444, 1, mpo)

    @responses.activate
    def test_tournament_results(self):
        mpo = Division.objects.create(id='MPO')
        manolo = Friend.objects.create(username='manolo', gt_number=1922)
        fede = Friend.objects.create(username='fede', gt_number=2106)

        add_list_page([])
        add_rating_page(1922, [333])
        add_rating_page(2106, [333, 444])
        add_details_page(333, 'Test Tournament #3', '24.07.2021 - 25.07.2021')
        add_results_page(333, [1, 2, 1922, 4, 5, 2106])
        add_details_page(444, 'Test Tournament #4', '26.07.2021')
        add_results_page(444, [2106, 2, 3], dnf=[1922])

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(2)
        self.assert_results_amount(3)
        self.assert_result(manolo, 333, 3, mpo)
        self.assert_result(fede, 333, 6, mpo)
        self.assert_result(fede, 444, 1, mpo)

    @responses.activate
    def test_tournament_results_with_existing_tournament(self):
        mpo = Division.objects.create(id='MPO')
        manolo = Friend.objects.create(username='manolo', gt_number=1922)
        fede = Friend.objects.create(username='fede', gt_number=2106)
        Tournament.objects.create(gt_id=333, name='Test Tournament #3', begin=PAST_JULY_24, end=PAST_JULY_25)

        add_list_page([])
        add_rating_page(1922, [333])
        add_rating_page(2106, [333, 444])
        add_details_page(333, 'Test Tournament #3', '24.07.2021 - 25.07.2021')
        add_results_page(333, [1, 2, 1922, 4, 5, 2106])
        add_details_page(444, 'Test Tournament #4', '26.07.2021')
        add_results_page(444, [2106, 2, 3], dnf=[1922])

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(2)
        self.assert_results_amount(3)
        self.assert_result(manolo, 333, 3, mpo)
        self.assert_result(fede, 333, 6, mpo)
        self.assert_result(fede, 444, 1, mpo)

    @responses.activate
    def test_tournament_results_with_existing_results(self):
        mpo = Division.objects.create(id='MPO')
        manolo = Friend.objects.create(username='manolo', gt_number=1922)
        fede = Friend.objects.create(username='fede', gt_number=2106)
        tournament_3 = Tournament.objects.create(gt_id=333, name='Test Tournament #3',
                                                 begin=PAST_JULY_24, end=PAST_JULY_25)
        Result.objects.create(friend=fede, tournament=tournament_3, position=6, division=mpo)

        add_list_page([])
        add_rating_page(1922, [333])
        add_rating_page(2106, [333, 444])
        add_details_page(333, 'Test Tournament #3', '24.07.2021 - 25.07.2021')
        add_results_page(333, [1, 2, 1922, 4, 5, 2106])
        add_details_page(444, 'Test Tournament #4', '26.07.2021')
        add_results_page(444, [2106, 2, 3], dnf=[1922])

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(2)
        self.assert_results_amount(3)
        self.assert_result(manolo, 333, 3, mpo)
        self.assert_result(fede, 333, 6, mpo)
        self.assert_result(fede, 444, 1, mpo)

    @responses.activate
    def test_tournament_results_with_broken_page(self):
        Friend.objects.create(username='manolo', gt_number=1922)

        add_list_page([])
        add_rating_page(1922, [333])
        add_details_page(333, 'Test Tournament #3', '24.07.2021 - 25.07.2021')
        add_results_page(333, [1, 2, 1922, 4, 5, 2106], broken=True)

        try:
            german_tour.update_all_tournaments()
            self.fail('This should have thrown an exception')
        except ColumnNotFound as error:
            self.assertEqual(error.text, 'Division ')

    @responses.activate
    def test_tournament_with_old_url_from_rating_page(self):
        mpo = Division.objects.create(id='MPO')
        manolo = Friend.objects.create(username='manolo', gt_number=1922)

        add_list_page([])
        add_rating_page(1922, [333], include_old_url=True)
        add_details_page(333, 'Test Tournament #3', '24.07.2021 - 25.07.2021')
        add_results_page(333, [1, 2, 1922])

        german_tour.update_all_tournaments()

        self.assert_tournament_amount(1)
        self.assert_results_amount(1)
        self.assert_result(manolo, 333, 3, mpo)

    @responses.activate
    def test_tournament_with_unknown_url_from_rating_page(self):
        Division.objects.create(id='MPO')
        Friend.objects.create(username='manolo', gt_number=1922)

        add_list_page([])
        add_rating_page(1922, [333], include_unknown_url=True)

        try:
            german_tour.update_all_tournaments()
            self.fail('This should have thrown an exception')
        except ValueError as error:
            self.assertEqual(error.args[0], 'Tournament URL not recognized: http://wft-richard.com/123')

    @responses.activate
    def test_results_from_one_tournament(self):
        mpo = Division.objects.create(id='MPO')
        manolo = Friend.objects.create(username='manolo', gt_number=1922)
        tournament = Tournament.objects.create(gt_id=333, name='Test Tournament #3',
                                               begin=PAST_JULY_24, end=PAST_JULY_25)

        add_details_page(333, 'Test Tournament #3', '24.07.2021 - 25.07.2021')
        add_results_page(333, [1, 2, 1922])

        german_tour.update_tournament_results(tournament)

        self.assert_tournament_amount(1)
        self.assert_results_amount(1)
        self.assert_result(manolo, 333, 3, mpo)

    def assert_results_amount(self, amount):
        self.assertEqual(Result.objects.all().count(), amount, f'there should be {amount} Result objects')

    def assert_result(self, friend, tournament_id, position, division):
        result = friend.results.get(tournament__gt_id=tournament_id)
        self.assertEqual(result.position, position, 'position does not match')
        self.assertEqual(result.division, division, 'division does not match')
