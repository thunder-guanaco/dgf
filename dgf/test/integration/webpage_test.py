from datetime import datetime, date
from unittest import TestCase

from django.test import Client, override_settings
from django.urls import reverse
from parameterized import parameterized

from dgf.models import Friend, Tournament, BagTagChange, Course, GitHubIssue, Tour

LOGGED_IN = True
NOT_LOGGED_IN = False


def get_test_friend():
    return Friend.objects.get_or_create(username='test_friend')[0]


def get_test_tournament():
    return Tournament.objects.get_or_create(name='Test Tournament',
                                            defaults={
                                                'begin': date.today(),
                                                'end': date.today()
                                            })[0]


def get_test_bag_tag_change():
    return BagTagChange.objects.get_or_create(actor=get_test_friend(),
                                              friend=get_test_friend(),
                                              new_number=1,
                                              previous_number=2,
                                              defaults={
                                                  'timestamp': datetime.now()
                                              })[0]


def get_test_course():
    return Course.objects.get_or_create(name='Test Course')[0]


def get_test_git_hub_issue():
    return GitHubIssue.objects.get_or_create(title='Test GitHub Issue')[0]


def get_test_tour():
    return Tour.objects.get_or_create(name='Test Tour')[0]


def get_id(obj):
    return obj.id


def get_slug(friend):
    return friend.slug


class WebpageTestCase(TestCase):

    @parameterized.expand([
        ('friend index - not logged in', NOT_LOGGED_IN, 'dgf:friend_index', 200),
        ('friend index - not logged in', LOGGED_IN, 'dgf:friend_index', 200),

        ('friend detail - not logged in', NOT_LOGGED_IN, ('dgf:friend_detail', get_test_friend, get_slug), 200),
        ('friend detail - not logged in', LOGGED_IN, ('dgf:friend_detail', get_test_friend, get_slug), 200),

        ('friend update - not logged in', NOT_LOGGED_IN, 'dgf:friend_update', (302, '/login')),
        ('friend update - not logged in', LOGGED_IN, 'dgf:friend_update', 200),

        ('feedback - not logged in', NOT_LOGGED_IN, 'dgf:feedback', (302, '/login')),
        ('feedback - not logged in', LOGGED_IN, 'dgf:feedback', 200),

        ('media - not logged in', NOT_LOGGED_IN, 'dgf:media', 200),
        ('media - not logged in', LOGGED_IN, 'dgf:media', 200),

        ('tournament index - not logged in', NOT_LOGGED_IN, 'dgf:tournament_index', (302, '/login')),
        ('tournament index - not logged in', LOGGED_IN, 'dgf:tournament_index', 200),

        ('TS next tournaments - not logged in', NOT_LOGGED_IN, 'dgf:tremonia_series_next_tournament',
         (302, 'https://discgolfmetrix.com/')),
        ('TS next tournaments - not logged in', LOGGED_IN, 'dgf:tremonia_series_next_tournament',
         (302, 'https://discgolfmetrix.com/')),

        ('TS future dates - not logged in', NOT_LOGGED_IN, 'dgf:tremonia_series_future_dates', 200),
        ('future dates - not logged in', LOGGED_IN, 'dgf:tremonia_series_future_dates', 200),

        ('login - not logged in', NOT_LOGGED_IN, 'login', 200),
        ('login - not logged in', LOGGED_IN, 'login', 200),

        ('logout - not logged in', NOT_LOGGED_IN, 'logout', (302, '/')),
        ('logout - not logged in', LOGGED_IN, 'logout', (302, '/')),

        ('cookie consent index - not logged in', NOT_LOGGED_IN, 'cookie_consent_cookie_group_list', 200),
        ('cookie consent index - not logged in', LOGGED_IN, 'cookie_consent_cookie_group_list', 200),

        ('friend admin - not logged in', NOT_LOGGED_IN, 'admin:dgf_friend_changelist', (302, '/admin/login')),

        ('friend admin list - not logged in', LOGGED_IN, 'admin:dgf_friend_changelist', 200),
        ('friend admin add - not logged in', LOGGED_IN, 'admin:dgf_friend_add', 200),
        ('friend admin change - not logged in', LOGGED_IN, ('admin:dgf_friend_change', get_test_friend, get_id), 200),

        ('tournament admin list - not logged in', LOGGED_IN, 'admin:dgf_tournament_changelist', 200),
        ('tournament admin add - not logged in', LOGGED_IN, 'admin:dgf_tournament_add', 200),
        ('tournament admin change - not logged in', LOGGED_IN,
         ('admin:dgf_tournament_change', get_test_tournament, get_id),
         200),

        ('bag tag change admin list - not logged in', LOGGED_IN, 'admin:dgf_bagtagchange_changelist', 200),
        ('bag tag change admin add - not logged in', LOGGED_IN, 'admin:dgf_bagtagchange_add', 200),
        ('bag tag change admin change - not logged in', LOGGED_IN,
         ('admin:dgf_bagtagchange_change', get_test_bag_tag_change, get_id), 200),

        ('course admin list - not logged in', LOGGED_IN, 'admin:dgf_course_changelist', 200),
        ('course admin add - not logged in', LOGGED_IN, 'admin:dgf_course_add', 200),
        ('course admin change - not logged in', LOGGED_IN, ('admin:dgf_course_change', get_test_course, get_id), 200),

        ('github issue admin list - not logged in', LOGGED_IN, 'admin:dgf_githubissue_changelist', 200),
        ('github issue admin add - not logged in', LOGGED_IN, 'admin:dgf_githubissue_add', 200),
        ('github issue admin change - not logged in', LOGGED_IN,
         ('admin:dgf_githubissue_change', get_test_git_hub_issue, get_id), 200),

        ('tour admin list - not logged in', LOGGED_IN, 'admin:dgf_tour_changelist', 200),
        ('tour admin add - not logged in', LOGGED_IN, 'admin:dgf_tour_add', 200),
        ('tour admin change - not logged in', LOGGED_IN, ('admin:dgf_tour_change', get_test_tour, get_id), 200),
    ])
    @override_settings(ROOT_URLCONF='dgf.test.urls')
    def test_dgf_pages(self, name, logged_in, url, expected):

        client = Client()
        if logged_in:
            self.login(client)

        if type(url) == tuple:
            url_name, get_obj, get_field = url
            args = [get_field(get_obj())]
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
