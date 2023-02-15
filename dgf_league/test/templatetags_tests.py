from unittest import TestCase

from dgf_league.models import Team
from dgf_league.templatetags.dgf_league import calculate_positions


def create_team(points):
    team = Team()
    team.points = points
    return team


def create_teams(points):
    return [create_team(n) for n in points]


class TemplatetagsTests(TestCase):

    def test_calculate_positions(self):
        self.assertTeams(points=[10, 9, 8, 7, 6], expected_positions=[1, 2, 3, 4, 5])
        self.assertTeams(points=[0, 0, 0, 0, 0], expected_positions=[1, 1, 1, 1, 1])
        self.assertTeams(points=[10, 5, 0, 0, 0], expected_positions=[1, 2, 3, 3, 3])
        self.assertTeams(points=[10, 10, 0, 0, 0], expected_positions=[1, 1, 3, 3, 3])
        self.assertTeams(points=[10, 10, 5, 5, 0], expected_positions=[1, 1, 3, 3, 5])
        self.assertTeams(points=[10, 9, 5, 5, 0], expected_positions=[1, 2, 3, 3, 5])

    def assertTeams(self, points, expected_positions):
        if points is None:
            points = []
        if expected_positions is None:
            expected_positions = []

        teams = create_teams(points)
        teams_with_positions = calculate_positions(teams)
        positions = [team.position for team in teams_with_positions]
        self.assertEqual(positions, expected_positions, msg='Unexpected positions')
