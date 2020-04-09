from django.test import TestCase

from ..apps import update_approved_discs
from ..models import Disc


class DiscModelsTest(TestCase):

    def test_discs_are_loaded(self):
        update_approved_discs()
        pd3 = Disc.objects.get(model='PD3')
        self.assertEqual(pd3.mold, 'PD3')
        self.assertEqual(pd3.manufacturer, 'Discmania')
