from parameterized import parameterized

from dgf.test.integration.basic_view_test import BasicViewsTest


class BasicTremoniaSeriesViewsTest(BasicViewsTest):

    @parameterized.expand([
        ('GET Index', 'GET', 'dgf_tremonia_series:index', 200),
        ('GET Includes', 'GET', 'dgf_tremonia_series:next-tournaments-include', 200),
    ])
    def test_dgf_views(self, name, method, url, expected):
        super().test_dgf_views(self, name, method, url)
