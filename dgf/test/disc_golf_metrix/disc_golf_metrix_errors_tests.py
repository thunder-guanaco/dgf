from django.test import TestCase

from dgf.disc_golf_metrix.disc_golf_metrix import DiscGolfMetrixImporter


class IncompleteDiscGolfMetrixImporter(DiscGolfMetrixImporter):

    def extract_name(self, dgm_tournament):
        return ''

    def generate_tours(self, tournament):
        return []


class DiscGolfMetrixErrors(TestCase):
    def setUp(self):
        pass

    def test_no_root_id(self):
        with self.assertRaises(NotImplementedError) as context_manager:
            IncompleteDiscGolfMetrixImporter().update_tournaments()
        self.assertEqual(context_manager.exception.args[0], 'root_id must be defined!')
