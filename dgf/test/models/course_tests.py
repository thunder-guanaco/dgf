
from django.test import TestCase

from ...models import Course


class CourseModelTest(TestCase):

    def test_representation(self):
        # no city - no country
        self.assert_representation(expected='Wischlingen',
                                   name='Wischlingen', city=None, country=None)

        # no city - empty country
        self.assert_representation(expected='Wischlingen',
                                   name='Wischlingen', city=None, country='')

        # empty city - no country
        self.assert_representation(expected='Wischlingen',
                                   name='Wischlingen', city='', country=None)

        # empty city - empty country
        self.assert_representation(expected='Wischlingen',
                                   name='Wischlingen', city='', country='')

        # no city - DE
        self.assert_representation(expected='Wischlingen',
                                   name='Wischlingen', city=None, country='DE')

        # empty city - DE
        self.assert_representation(expected='Wischlingen',
                                   name='Wischlingen', city='', country='DE')

        # same name as city - DE
        self.assert_representation(expected='Fröndenberg',
                                   name='Fröndenberg', city='Fröndenberg', country='DE')

        # name contains city - DE
        self.assert_representation(expected='Volkspark Potsdam',
                                   name='Volkspark Potsdam', city='Potsdam', country='DE')

        # city contains name - DE
        self.assert_representation(expected='Söhnstetten',
                                   name='Söhnstetten', city='Steinheim - Söhnstetten', country='DE')

        # name contains part city and city contains name - DE
        self.assert_representation(expected='Söhnstetten (Albuch Classic)',
                                   name='Söhnstetten (Albuch Classic)', city='Steinheim - Söhnstetten', country='DE')

        # name and city are completely different - DE
        self.assert_representation(expected='Wischlingen (Dortmund)',
                                   name='Wischlingen', city='Dortmund', country='DE')

        # no city - ES
        self.assert_representation(expected='Mijas (ES)',
                                   name='Mijas', city=None, country='ES')

        # empty city - ES
        self.assert_representation(expected='Mijas (ES)',
                                   name='Mijas', city='', country='ES')

        # same name as city - ES
        self.assert_representation(expected='Mijas (ES)',
                                   name='Mijas', city='Mijas', country='ES')

        # name contains city - ES
        self.assert_representation(expected='DiscGolfPark Mijas (ES)',
                                   name='DiscGolfPark Mijas', city='Mijas', country='ES')

        # city contains name - ES
        self.assert_representation(expected='Mijas (ES)',
                                   name='Mijas', city='Mijas, Málaga', country='ES')

        # name contains part city and city contains name - DE
        self.assert_representation(expected='DiscGolfPark Mijas (ES)',
                                   name='DiscGolfPark Mijas', city='Mijas, Málaga', country='ES')

        # name contains part city and city contains name - DE (parenthesis)
        self.assert_representation(expected='DiscGolfPark Mijas (ES)',
                                   name='DiscGolfPark Mijas', city='Málaga (Mijas)', country='ES')

        # name and city are completely different - ES
        self.assert_representation(expected='Purificación Tomás (Oviedo, ES)',
                                   name='Purificación Tomás', city='Oviedo', country='ES')

    def assert_representation(self, expected, **fields):
        course = Course(**fields)
        self.assertEqual(str(course), expected)
