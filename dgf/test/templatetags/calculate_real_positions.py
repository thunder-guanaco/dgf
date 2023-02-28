from dataclasses import dataclass
from unittest import TestCase

from dgf.templatetags.dgf import calculate_real_positions


@dataclass
class TestResult:
    points: int


def create_results(points):
    return [TestResult(n) for n in points]


def set_position(result, position):
    result.position = position


class CalculateRealPositionsTest(TestCase):

    def test_calculate_real_positions(self):
        self.assertRealPositions(points=[20, 17, 15, 10, 7], expected_positions=[1, 2, 3, 4, 5])
        self.assertRealPositions(points=[20, 20, 15, 10, 7], expected_positions=[1, 1, 3, 4, 5])
        self.assertRealPositions(points=[0, 0, 0, 0, 0], expected_positions=[1, 1, 1, 1, 1])
        self.assertRealPositions(points=[10, 0, 0, 0, 0], expected_positions=[1, 2, 2, 2, 2])
        self.assertRealPositions(points=[10, 10, 5, 5, 0], expected_positions=[1, 1, 3, 3, 5])
        self.assertRealPositions(points=[10, 9, 5, 5, 0], expected_positions=[1, 2, 3, 3, 5])
        self.assertRealPositions(points=[0], expected_positions=[1])
        self.assertRealPositions(points=[10], expected_positions=[1])
        self.assertRealPositions(points=[], expected_positions=[])

    def assertRealPositions(self, points, expected_positions):
        results = create_results(points)
        results_with_positions = calculate_real_positions(results, lambda x: x.points, set_position)

        positions = [result.position for result in results_with_positions]
        self.assertEqual(positions, expected_positions, msg='Unexpected positions')
