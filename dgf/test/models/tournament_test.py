from datetime import datetime

from django.test import TestCase

from dgf.models import Friend, Tournament, Result

IS_OK = True
NOT_OK = False


class TournamentModelTest(TestCase):

    def test_repeated_first_positions(self):
        tournament = self.create_tournament()
        for_friends = self.create_friends(4)
        self.assert_that(tournament, IS_OK, for_friends, in_positions=[])  # empty results
        self.assert_that(tournament, IS_OK, for_friends, in_positions=[1, 2, 3, 4])
        self.assert_that(tournament, NOT_OK, for_friends, in_positions=[1, 2, 3, 3])
        self.assert_that(tournament, NOT_OK, for_friends, in_positions=[1, 2, 2, 3])
        self.assert_that(tournament, NOT_OK, for_friends, in_positions=[1, 2, 2, 4])
        self.assert_that(tournament, NOT_OK, for_friends, in_positions=[1, 2, 2, 2])
        self.assert_that(tournament, NOT_OK, for_friends, in_positions=[1, 1, 3, 4])
        self.assert_that(tournament, NOT_OK, for_friends, in_positions=[1, 1, 3, 3])
        self.assert_that(tournament, NOT_OK, for_friends, in_positions=[1, 1, 1, 2])
        self.assert_that(tournament, NOT_OK, for_friends, in_positions=[1, 1, 1, 3])
        self.assert_that(tournament, NOT_OK, for_friends, in_positions=[1, 1, 1, 4])
        self.assert_that(tournament, NOT_OK, for_friends, in_positions=[1, 1, 1, 1])

    def assert_that(self, tournament, ok, for_friends, in_positions):
        Result.objects.all().delete()
        self.create_result(tournament, for_friends, in_positions)

        nt = 'n\'t' if not ok else ''
        self.assertEqual(tournament.first_positions_are_ok, ok,
                         msg=f'Tournament with positions {in_positions} should{nt} be ok')

    def create_tournament(self):
        Tournament.objects.all().delete()
        return Tournament.objects.create(name='test', begin=datetime.today(), end=datetime.today())

    def create_friends(self, amount):
        Friend.objects.all().delete()
        return [Friend.objects.create(username=f'test_{i}',
                                      first_name=f'test_{i}') for i
                in range(amount)]

    def create_result(self, tournament, friends, positions):
        for i, position in enumerate(positions):
            Result.objects.create(tournament=tournament, friend=friends[i], position=position)
