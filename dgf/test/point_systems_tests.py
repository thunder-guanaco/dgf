from django.test import TestCase
from parameterized import parameterized

from dgf.models import Tour, Result, Tournament, Friend
from dgf.point_systems import calculate_points
from dgf.test.models.creator import create_friends, create_tournaments


class PointSystemsTest(TestCase):

    def setUp(self):
        Tournament.objects.all().delete()
        Friend.objects.all().delete()
        Tour.objects.all().delete()

    def test_calculate_points_without_point_system(self):
        self.assert_points(point_system=None,
                           positions=[1, 2],
                           points=[None, None])

    def test_calculate_points_with_empty_point_system(self):
        self.assert_points(point_system='',
                           positions=[1, 2],
                           points=[None, None])

    def test_calculate_points_with_unknown_point_system(self):
        self.assert_points(point_system='unknown_point_system',
                           positions=[1, 2],
                           points=[None, None])

    @parameterized.expand([
        (1, [20]),
        (2, [20, 17]),
        (3, [21, 17, 15]),
        (4, [21, 18, 15, 10]),
        (5, [22, 18, 16, 10, 7]),
        (6, [22, 19, 16, 11, 7, 5]),
        (7, [23, 19, 17, 11, 8, 5, 4]),
        (8, [23, 20, 17, 12, 8, 6, 4, 3]),
        (9, [24, 20, 18, 12, 9, 6, 5, 3, 2]),
        (10, [24, 21, 18, 13, 9, 7, 5, 4, 2, 1]),
        (11, [25, 21, 19, 13, 10, 7, 6, 4, 3, 1, 0]),
        (12, [25, 22, 19, 14, 10, 8, 6, 5, 3, 2, 0, 0]),
        (13, [26, 22, 20, 14, 11, 8, 7, 5, 4, 2, 1, 0, 0]),
        (14, [26, 23, 20, 15, 11, 9, 7, 6, 4, 3, 1, 1, 0, 0]),
        (15, [27, 23, 21, 15, 12, 9, 8, 6, 5, 3, 2, 1, 1, 0, 0]),
        (16, [27, 24, 21, 16, 12, 10, 8, 7, 5, 4, 2, 2, 1, 1, 0, 0]),
        (17, [28, 24, 22, 16, 13, 10, 9, 7, 6, 4, 3, 2, 2, 1, 1, 0, 0]),
        (18, [28, 25, 22, 17, 13, 11, 9, 8, 6, 5, 3, 3, 2, 2, 1, 1, 0, 0]),
        (19, [29, 25, 23, 17, 14, 11, 10, 8, 7, 5, 4, 3, 3, 2, 2, 1, 1, 0, 0]),
        (20, [29, 26, 23, 18, 14, 12, 10, 9, 7, 6, 4, 4, 3, 3, 2, 2, 1, 1, 0, 0]),
    ])
    def test_calculate_points(self, amount_of_players, expected_points):
        self.assert_points(point_system=Tournament.TS_POINTS_WITH_BEATEN_PLAYERS,
                           positions=list(range(1, amount_of_players + 1)),
                           points=expected_points)

    def assert_points(self, point_system, positions, points):
        self.assertEqual(len(positions), len(points),
                         msg='This test makes no sense: there is not the same number of positions and points')
        friends = create_friends(len(positions))
        if len(positions) == 1:
            friends = [friends]
        tournament = create_tournaments(1)
        tournament.point_system = point_system
        tournament.save()
        results = [Result.objects.create(tournament=tournament,
                                         friend=friends[i],
                                         position=position)
                   for i, position in enumerate(positions)]

        for i, position in enumerate(positions):
            self.assertEqual(calculate_points(results[i]), points[i],
                             msg=f'positon {position} should result in {points[i]} points')
