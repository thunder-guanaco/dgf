from unittest import TestCase

from django.test import Client, override_settings
from django.urls import reverse
from parameterized import parameterized

from dgf.models import Friend
from dgf.test.models.creator import create_tours, create_git_hub_issues, create_courses, create_bag_tag_changes, \
    create_tournaments

LOGGED_IN = True
NOT_LOGGED_IN = False

test_friend, _ = Friend.objects.get_or_create(username='test_friend')


class WebpageTestCase(TestCase):

    @parameterized.expand([
        ('not logged in friend index', NOT_LOGGED_IN, 'dgf:friend_index', 200),
        ('logged in friend index', LOGGED_IN, 'dgf:friend_index', 200),

        ('not logged in friend detail', NOT_LOGGED_IN, ('dgf:friend_detail', [test_friend.slug]), 200),
        ('logged in friend detail', LOGGED_IN, ('dgf:friend_detail', [test_friend.slug]), 200),

        ('not logged in friend update', NOT_LOGGED_IN, 'dgf:friend_update', (302, '/login')),
        ('logged in friend update', LOGGED_IN, 'dgf:friend_update', 200),

        ('not logged in feedback', NOT_LOGGED_IN, 'dgf:feedback', (302, '/login')),
        ('logged in feedback', LOGGED_IN, 'dgf:feedback', 200),

        ('not logged in media', NOT_LOGGED_IN, 'dgf:media', 200),
        ('logged in media', LOGGED_IN, 'dgf:media', 200),

        ('not logged in tournament index', NOT_LOGGED_IN, 'dgf:tournament_index', (302, '/login')),
        ('logged in tournament index', LOGGED_IN, 'dgf:tournament_index', 200),

        ('not logged in TS next tournaments', NOT_LOGGED_IN, 'dgf:tremonia_series_next_tournament',
         (302, 'https://discgolfmetrix.com/')),
        ('logged in TS next tournaments', LOGGED_IN, 'dgf:tremonia_series_next_tournament',
         (302, 'https://discgolfmetrix.com/')),

        ('not logged in TS future dates', NOT_LOGGED_IN, 'dgf:tremonia_series_future_dates', 200),
        ('logged in future dates', LOGGED_IN, 'dgf:tremonia_series_future_dates', 200),

        ('not logged in login', NOT_LOGGED_IN, 'login', 200),
        ('logged in login', LOGGED_IN, 'login', 200),

        ('not logged in logout', NOT_LOGGED_IN, 'logout', (302, '/')),
        ('logged in logout', LOGGED_IN, 'logout', (302, '/')),

        ('not logged in cookie consent index', NOT_LOGGED_IN, 'cookie_consent_cookie_group_list', 200),
        ('logged in cookie consent index', LOGGED_IN, 'cookie_consent_cookie_group_list', 200),

        ('not logged in friend admin', NOT_LOGGED_IN, 'admin:dgf_friend_changelist', (302, '/admin/login')),

        ('logged in friend admin list', LOGGED_IN, 'admin:dgf_friend_changelist', 200),
        ('logged in friend admin add', LOGGED_IN, 'admin:dgf_friend_add', 200),
        ('logged in friend admin change', LOGGED_IN, ('admin:dgf_friend_change', [test_friend.id]), 200),

        ('logged in tournament admin list', LOGGED_IN, 'admin:dgf_tournament_changelist', 200),
        ('logged in tournament admin add', LOGGED_IN, 'admin:dgf_tournament_add', 200),
        ('logged in tournament admin change', LOGGED_IN, ('admin:dgf_tournament_change', [create_tournaments(1).id]),
         200),

        ('logged in bag tag change admin list', LOGGED_IN, 'admin:dgf_bagtagchange_changelist', 200),
        ('logged in bag tag change admin add', LOGGED_IN, 'admin:dgf_bagtagchange_add', 200),
        ('logged in bag tag change admin change', LOGGED_IN,
         ('admin:dgf_bagtagchange_change', [create_bag_tag_changes(1).id]), 200),

        ('logged in course admin list', LOGGED_IN, 'admin:dgf_course_changelist', 200),
        ('logged in course admin add', LOGGED_IN, 'admin:dgf_course_add', 200),
        ('logged in course admin change', LOGGED_IN, ('admin:dgf_course_change', [create_courses(1).id]), 200),

        ('logged in github issue admin list', LOGGED_IN, 'admin:dgf_githubissue_changelist', 200),
        ('logged in github issue admin add', LOGGED_IN, 'admin:dgf_githubissue_add', 200),
        ('logged in github issue admin change', LOGGED_IN,
         ('admin:dgf_githubissue_change', [create_git_hub_issues(1).id]), 200),

        ('logged in tour admin list', LOGGED_IN, 'admin:dgf_tour_changelist', 200),
        ('logged in tour admin add', LOGGED_IN, 'admin:dgf_tour_add', 200),
        ('logged in tour admin change', LOGGED_IN, ('admin:dgf_tour_change', [create_tours(1).id]), 200),
    ])
    @override_settings(ROOT_URLCONF='dgf.test.urls')
    def test_dgf_pages(self, name, logged_in, url, expected):

        client = Client()
        if logged_in:
            self.login(client)

        if type(url) == tuple:
            url_name, args = url
        else:
            url_name = url
            args = []

        response = client.get(reverse(url_name, args=args))

        if type(expected) == tuple:
            expected_status_code, expected_url = expected
        else:
            expected_status_code = expected
            expected_url = None

        self.assertEqual(response.status_code, expected_status_code, msg=f'Unexpected status code for URL {url}')
        if expected_url:
            self.assertTrue(response.url.startswith(expected_url))

    @override_settings(ROOT_URLCONF='dgf.test.urls')
    def atest_update_profile(self):
        client = Client()
        self.login(client)
        response = client.post(reverse('dgf:friend_update'))

        self.assertEqual(response.status_code, 200)

    def login(self, client):
        friend, created = Friend.objects.get_or_create(username='friend')
        friend.set_password('12345')
        friend.is_superuser = True
        friend.is_staff = True
        friend.save()
        client.login(username='friend', password='12345')
