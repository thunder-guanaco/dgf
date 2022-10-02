from unittest import TestCase

import responses

from dgf.models import Tournament, Friend


class GermanTourTest(TestCase):

    def setUp(self):
        Friend.objects.all().delete()
        Tournament.objects.all().delete()
        responses.reset()

    def assert_tournament_amount(self, amount):
        self.assertEqual(Tournament.objects.all().count(), amount, f'there should be {amount} Tournament objects')

    def assert_tournament_exists(self, gt_id, name, begin, end, url, pdga_id=None, metrix_id=None):
        if gt_id:
            tournament = Tournament.objects.get(gt_id=gt_id)
            self.assertEqual(tournament.pdga_id, pdga_id, 'pdga_id does not match')
        elif pdga_id:
            tournament = Tournament.objects.get(pdga_id=pdga_id)
            self.assertIsNone(tournament.gt_id, 'gt_id should be None')
        elif metrix_id:
            tournament = Tournament.objects.get(metrix_id=metrix_id)
            self.assertIsNone(tournament.gt_id, 'gt_id should be None')
        else:
            self.fail('set either gt_id, pdga_id or mix_id')
        self.assertEqual(tournament.name, name, 'name does not match')
        self.assertEqual(tournament.begin, begin, 'begin does not match')
        self.assertEqual(tournament.end, end, 'end does not match')
        self.assertEqual(tournament.url, url, 'url does not match')

    def assert_tournament_does_not_exists(self, gt_id):
        with self.assertRaises(Tournament.DoesNotExist):
            Tournament.objects.get(gt_id=gt_id)
