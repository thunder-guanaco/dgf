import responses

from dgf import pdga
from dgf.models import Friend, Result, Division, Tournament
from dgf.test.pdga.tournaments.pdga_tournament_test import PdgaTournamentTest, JULY_24, JULY_25, JULY_26, APRIL_2
from dgf.test.pdga.tournaments.responses import add_year_links, add_results, add_tournament_data
from dgf_cms.settings import PDGA_EVENT_URL


class PdgaResultsTest(PdgaTournamentTest):

    @responses.activate
    def setUp(self):
        super().setUp()
        Result.objects.all().delete()
        Division.objects.all().delete()

    def test_no_results(self):
        manolo = Friend.objects.create(username='manolo', pdga_number=111828)

        add_year_links(111828, years=[])

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        self.assert_results_amount(0)

    def test_results(self):
        ma3 = Division.objects.create(id='MA3')
        mpo = Division.objects.create(id='MPO')
        manolo = Friend.objects.create(username='manolo', pdga_number=111828)

        add_year_links(111828, years=[2022, 2021])
        add_results(111828, 2022, [(1111, 1, 'MA3'), (2222, 2, 'MPO')])
        add_results(111828, 2021, [(3333, 3, 'MPO')])
        add_tournament_data('1111', 'Tremonia Series #1', '2021-07-24', '2021-07-24')
        add_tournament_data('2222', 'Tremonia Series #2', '2021-07-25', '2021-07-25')
        add_tournament_data('3333', 'Tremonia Series #3', '2021-07-26', '2021-07-26')

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        self.assert_tournament_amount(3)
        self.assert_tournament_exists(1111, 'Tremonia Series #1', JULY_24, JULY_24, PDGA_EVENT_URL.format(1111))
        self.assert_tournament_exists(2222, 'Tremonia Series #2', JULY_25, JULY_25, PDGA_EVENT_URL.format(2222))
        self.assert_tournament_exists(3333, 'Tremonia Series #3', JULY_26, JULY_26, PDGA_EVENT_URL.format(3333))

        self.assert_results_amount(3)
        self.assert_result(manolo, 1111, 1, ma3)
        self.assert_result(manolo, 2222, 2, mpo)
        self.assert_result(manolo, 3333, 3, mpo)

    # test german tour override results!

    def test_results_with_existing_tournament(self):
        mpo = Division.objects.create(id='MPO')
        manolo = Friend.objects.create(username='manolo', pdga_number=111828)
        Tournament.objects.create(pdga_id=1111, name='Tremonia Series #1', begin=JULY_24, end=JULY_24)

        add_year_links(111828, years=[2022])
        add_results(111828, 2022, [(1111, 1, 'MPO')])
        add_tournament_data('1111', 'Tremonia Series #1', '2021-07-24', '2021-07-24')

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(1111, 'Tremonia Series #1', JULY_24, JULY_24, PDGA_EVENT_URL.format(1111))

        self.assert_results_amount(1)
        self.assert_result(manolo, 1111, 1, mpo)

    def test_results_with_existing_tournament_and_result_with_legacy_division(self):
        manolo = Friend.objects.create(username='manolo', pdga_number=111828)
        Tournament.objects.create(pdga_id=1111, name='Tremonia Series #1', begin=JULY_24, end=JULY_24)

        add_year_links(111828, years=[2022])
        add_results(111828, 2022, [(1111, 1, 'MJ1')])
        add_tournament_data('1111', 'Tremonia Series #1', '2021-07-24', '2021-07-24')

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(1111, 'Tremonia Series #1', JULY_24, JULY_24, PDGA_EVENT_URL.format(1111))

        self.assert_results_amount(1)
        self.assert_result(manolo, 1111, 1, Division(id='MJ1'))

    def test_results_with_existing_tournament_update_name(self):
        Division.objects.create(id='MPO')
        manolo = Friend.objects.create(username='manolo', pdga_number=111828)
        Tournament.objects.create(pdga_id=1111, name='Tremonia Series #1', begin=JULY_24, end=JULY_24)

        add_year_links(111828, years=[2022])
        add_results(111828, 2022, [(1111, 1, 'MPO')])
        add_tournament_data('1111', 'TS #1', '2021-07-24', '2021-07-24')

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(1111, 'TS #1', JULY_24, JULY_24, PDGA_EVENT_URL.format(1111))

    def test_results_with_existing_tournament_update_dates(self):
        Division.objects.create(id='MPO')
        manolo = Friend.objects.create(username='manolo', pdga_number=111828)
        Tournament.objects.create(pdga_id=1111, name='Tremonia Series #1', begin=JULY_24, end=JULY_24)

        add_year_links(111828, years=[2022])
        add_results(111828, 2022, [(1111, 1, 'MPO')])
        add_tournament_data('1111', 'TS #1', '2021-04-02', '2021-04-02')

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(1111, 'TS #1', APRIL_2, APRIL_2, PDGA_EVENT_URL.format(1111))

    def test_results_with_existing_tournament_and_result(self):
        mpo = Division.objects.create(id='MPO')
        manolo = Friend.objects.create(username='manolo', pdga_number=111828)
        ts1 = Tournament.objects.create(pdga_id=1111, name='Tremonia Series #1', begin=JULY_24, end=JULY_24)
        Result.objects.create(friend=manolo, tournament=ts1, position=1, division=mpo)

        add_year_links(111828, years=[2022])
        add_results(111828, 2022, [(1111, 1, 'MPO')])
        add_tournament_data('1111', 'Tremonia Series #1', '2021-07-24', '2021-07-24')

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(1111, 'Tremonia Series #1', JULY_24, JULY_24, PDGA_EVENT_URL.format(1111))

        self.assert_results_amount(1)
        self.assert_result(manolo, 1111, 1, mpo)

    def test_results_with_existing_tournament_and_result_with_different_position(self):
        mpo = Division.objects.create(id='MPO')
        manolo = Friend.objects.create(username='manolo', pdga_number=111828)
        ts1 = Tournament.objects.create(pdga_id=1111, name='Tremonia Series #1', begin=JULY_24, end=JULY_24)
        Result.objects.create(friend=manolo, tournament=ts1, position=2, division=mpo)

        add_year_links(111828, years=[2022])
        add_results(111828, 2022, [(1111, 1, 'MPO')])
        add_tournament_data('1111', 'Tremonia Series #1', '2021-07-24', '2021-07-24')

        pdga.update_friend_tournaments(manolo, self.pdga_api)

        self.assert_tournament_amount(1)
        self.assert_tournament_exists(1111, 'Tremonia Series #1', JULY_24, JULY_24, PDGA_EVENT_URL.format(1111))

        self.assert_results_amount(1)
        self.assert_result(manolo, 1111, 2, mpo)

    def assert_results_amount(self, amount):
        self.assertEqual(Result.objects.all().count(), amount, f'there should be {amount} Result objects')

    def assert_result(self, friend, tournament_id, position, division):
        result = friend.results.get(tournament__pdga_id=tournament_id)
        self.assertEqual(result.position, position, 'position does not match')
        self.assertEqual(result.division, division, 'division does not match')
