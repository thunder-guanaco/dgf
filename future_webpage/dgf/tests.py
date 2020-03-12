from django.test import TestCase
from .models import Friend
from .pdga import PdgaApi


class FriendModelTest(TestCase):

    def test_slug_with_different_fields(self):
        self.expect_slug('antonio123', username='antonio123')

        self.expect_slug('antonio', username='antonio123', first_name='Antonio')

        self.expect_slug('tono', username='antonio123', nickname='Toño')
        self.expect_slug('tono', username='antonio123', first_name='Antonio', nickname='Toño')

        self.expect_slug('tony', username='antonio123', slug='tony')
        self.expect_slug('tony', username='antonio123', first_name='Antonio', slug='tony')
        self.expect_slug('tony', username='antonio123', nickname='Toño', slug='tony')
        self.expect_slug('tony', username='antonio123', first_name='Antonio', nickname='Toño', slug='tony')

    def expect_slug(self, expected_slug, **fields):
        Friend.objects.all().delete()
        friend = Friend(**fields)
        friend.save()
        self.assertEqual(friend.slug, expected_slug)


class PdgaTest(TestCase):

    def test_basic_user_call(self):
        pdga = PdgaApi()
        manolo = pdga.query_player(pdga_number=111828)['players'][0]
        self.assertEqual(manolo['pdga_number'], '111828')
