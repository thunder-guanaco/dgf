from unittest import TestCase

from django.test import Client, override_settings
from django.urls import reverse
from parameterized import parameterized

from ...models import Friend


class AddTestCase(TestCase):

    @parameterized.expand([
        ('dgf:friend_index', []),
        ('dgf:friend_detail', ['test']),
        ('dgf:friend_update', []),
        ('dgf:feedback', []),
        ('dgf:media', []),
        ('dgf:tournament_index', []),
    ])
    @override_settings(ROOT_URLCONF='dgf.test.urls')
    def test_dgf_pages(self, url_name, args):
        self.create_test_friend()

        client = Client()
        client.login(username='test', password='12345')
        response = client.get(reverse(url_name, args=args))

        self.assertEqual(response.status_code, 200)

    @override_settings(ROOT_URLCONF='dgf.test.urls')
    def test_update_profile(self):
        self.create_test_friend()

        client = Client()
        client.login(username='test', password='12345')
        response = client.post(reverse('dgf:friend_update'))

        self.assertEqual(response.status_code, 200)

    def test_login(self):
        client = Client()
        response = client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        client = Client()
        response = client.get(reverse('logout'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def create_test_friend(self):
        Friend.objects.all().delete()
        friend = Friend.objects.create(username='test', slug='test')
        friend.set_password('12345')
        friend.save()
