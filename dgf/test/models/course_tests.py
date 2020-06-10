from django.test import TestCase

from ...models import Course


class CourseModelTest(TestCase):

    def test_representation(self):
        # same name as city - DE
        self.expect_representation(expected='Fröndenberg',
                                   name='Fröndenberg', city='Fröndenberg', country='DE')

        # name contains city - DE
        self.expect_representation(expected='Volkspark Potsdam',
                                   name='Volkspark Potsdam', city='Potsdam', country='DE')

        # city contains name - DE
        self.expect_representation(expected='Söhnstetten',
                                   name='Söhnstetten', city='Steinheim - Söhnstetten', country='DE')

        # name contains part city and city contains name - DE
        self.expect_representation(expected='Söhnstetten (Albuch Classic)',
                                   name='Söhnstetten (Albuch Classic)', city='Steinheim - Söhnstetten', country='DE')

        # name and city are completely different - DE
        self.expect_representation(expected='Wischlingen (Dortmund)',
                                   name='Wischlingen', city='Dortmund', country='DE')

        # same name as city - ES
        self.expect_representation(expected='Mijas (ES)',
                                   name='Mijas', city='Mijas', country='ES')

        # name contains city - ES
        self.expect_representation(expected='DiscGolfPark Mijas (ES)',
                                   name='DiscGolfPark Mijas', city='Mijas', country='ES')

        # city contains name - ES
        self.expect_representation(expected='Mijas (ES)',
                                   name='Mijas', city='Mijas, Málaga', country='ES')

        # name contains part city and city contains name - DE
        self.expect_representation(expected='DiscGolfPark Mijas (ES)',
                                   name='DiscGolfPark Mijas', city='Mijas, Málaga', country='ES')

        # name contains part city and city contains name - DE (parenthesis)
        self.expect_representation(expected='DiscGolfPark Mijas (ES)',
                                   name='DiscGolfPark Mijas', city='Málaga (Mijas)', country='ES')

        # name and city are completely different - ES
        self.expect_representation(expected='Purificación Tomás (Oviedo, ES)',
                                   name='Purificación Tomás', city='Oviedo', country='ES')

    def expect_representation(self, expected, **fields):
        course = Course(**fields)
        self.assertEqual(str(course), expected)
