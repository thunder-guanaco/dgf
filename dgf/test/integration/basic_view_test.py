from datetime import datetime, date

from django.test import override_settings
from django.urls import reverse
from parameterized import parameterized

from dgf.models import Friend, Tournament, BagTagChange, Course, GitHubIssue, Tour, Attendance
from dgf.test.integration.client_test import ClientTest

LOGGED_IN = True
NOT_LOGGED_IN = False


def get_test_friend():
    return Friend.objects.get_or_create(username='test_friend')[0]


def get_test_friend_with_bag_tag():
    friend = get_test_friend()
    friend.bag_tag = 2
    friend.save()
    return friend


def get_test_tournament():
    return Tournament.objects.get_or_create(name='Test Tournament',
                                            defaults={
                                                'begin': date.today(),
                                                'end': date.today()
                                            })[0]


def get_test_tournament_with_attendance():
    tournament = get_test_tournament()
    Attendance.objects.create(friend=Friend.objects.get(username='friend'),
                              tournament=tournament)
    return tournament


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


def get_bag_tag(friend):
    return friend.bag_tag


class BasicViewsTest(ClientTest):

    @parameterized.expand([
        ('GET friend index - not logged in', NOT_LOGGED_IN, 'GET', 'dgf:friend_index', 200),
        ('GET friend index - logged in', LOGGED_IN, 'GET', 'dgf:friend_index', 200),

        ('GET friend detail - not logged in', NOT_LOGGED_IN, 'GET', ('dgf:friend_detail', get_test_friend, get_slug),
         200),
        ('GET friend detail - logged in', LOGGED_IN, 'GET', ('dgf:friend_detail', get_test_friend, get_slug), 200),

        ('GET friend update - not logged in', NOT_LOGGED_IN, 'GET', 'dgf:friend_update', (302, '/login')),
        ('GET friend update - logged in', LOGGED_IN, 'GET', 'dgf:friend_update', 200),

        ('POST friend update - not logged in', NOT_LOGGED_IN, 'POST', 'dgf:friend_update', (302, '/login')),
        ('POST friend update - logged in', LOGGED_IN, 'POST', 'dgf:friend_update', 200),

        ('GET feedback - not logged in', NOT_LOGGED_IN, 'GET', 'dgf:feedback', (302, '/login')),
        ('GET feedback - logged in', LOGGED_IN, 'GET', 'dgf:feedback', 200),

        ('GET media - not logged in', NOT_LOGGED_IN, 'GET', 'dgf:media', 200),
        ('GET media - logged in', LOGGED_IN, 'GET', 'dgf:media', 200),

        ('GET tournament index - not logged in', NOT_LOGGED_IN, 'GET', 'dgf:tournament_index', (302, '/login')),
        ('GET tournament index - logged in', LOGGED_IN, 'GET', 'dgf:tournament_index', 200),

        ('GET next TS tournaments - not logged in', NOT_LOGGED_IN, 'GET', 'dgf:tremonia_series_next_tournament',
         (302, 'https://discgolfmetrix.com/')),
        ('GET next TS tournaments - logged in', LOGGED_IN, 'GET', 'dgf:tremonia_series_next_tournament',
         (302, 'https://discgolfmetrix.com/')),

        ('GET future TS dates - not logged in', NOT_LOGGED_IN, 'GET', 'dgf:tremonia_series_future_dates', 200),
        ('GET future TS dates - logged in', LOGGED_IN, 'GET', 'dgf:tremonia_series_future_dates', 200),

        ('GET login - not logged in', NOT_LOGGED_IN, 'GET', 'login', 200),
        ('GET login - logged in', LOGGED_IN, 'GET', 'login', 200),

        ('GET logout - not logged in', NOT_LOGGED_IN, 'GET', 'logout', (302, '/')),
        ('GET logout - logged in', LOGGED_IN, 'GET', 'logout', (302, '/')),

        ('GET cookie consent index - not logged in', NOT_LOGGED_IN, 'GET', 'cookie_consent_cookie_group_list', 200),
        ('GET cookie consent index - logged in', LOGGED_IN, 'GET', 'cookie_consent_cookie_group_list', 200),

        ('GET friend admin - not logged in', NOT_LOGGED_IN, 'GET', 'admin:dgf_friend_changelist',
         (302, '/admin/login')),

        ('GET friend admin list - logged in', LOGGED_IN, 'GET', 'admin:dgf_friend_changelist', 200),
        ('GET friend admin add - logged in', LOGGED_IN, 'GET', 'admin:dgf_friend_add', 200),
        ('GET friend admin change - logged in', LOGGED_IN, 'GET',
         ('admin:dgf_friend_change', get_test_friend, get_id), 200),

        ('GET tournament admin list - logged in', LOGGED_IN, 'GET', 'admin:dgf_tournament_changelist', 200),
        ('GET tournament admin add - logged in', LOGGED_IN, 'GET', 'admin:dgf_tournament_add', 200),
        ('GET tournament admin change - logged in', LOGGED_IN, 'GET',
         ('admin:dgf_tournament_change', get_test_tournament, get_id), 200),

        ('GET bag tag change admin list - logged in', LOGGED_IN, 'GET', 'admin:dgf_bagtagchange_changelist', 200),
        ('GET bag tag change admin add - logged in', LOGGED_IN, 'GET', 'admin:dgf_bagtagchange_add', 200),
        ('GET bag tag change admin change - logged in', LOGGED_IN, 'GET',
         ('admin:dgf_bagtagchange_change', get_test_bag_tag_change, get_id), 200),

        ('GET course admin list - logged in', LOGGED_IN, 'GET', 'admin:dgf_course_changelist', 200),
        ('GET course admin add - logged in', LOGGED_IN, 'GET', 'admin:dgf_course_add', 200),
        ('GET course admin change - logged in', LOGGED_IN, 'GET', ('admin:dgf_course_change', get_test_course, get_id),
         200),

        ('GET github issue admin list - logged in', LOGGED_IN, 'GET', 'admin:dgf_githubissue_changelist', 200),
        ('GET github issue admin add - logged in', LOGGED_IN, 'GET', 'admin:dgf_githubissue_add', 200),
        ('GET github issue admin change - logged in', LOGGED_IN, 'GET',
         ('admin:dgf_githubissue_change', get_test_git_hub_issue, get_id), 200),

        ('GET tour admin list - logged in', LOGGED_IN, 'GET', 'admin:dgf_tour_changelist', 200),
        ('GET tour admin add - logged in', LOGGED_IN, 'GET', 'admin:dgf_tour_add', 200),
        ('GET tour admin change - logged in', LOGGED_IN, 'GET', ('admin:dgf_tour_change', get_test_tour, get_id), 200),

        ('GET tournament attendance - not logged in', NOT_LOGGED_IN, 'GET',
         ('dgf:tournament_attendance', get_test_tournament, get_id), (302, '/login')),

        ('GET tournament attendance - logged in', LOGGED_IN, 'GET',
         ('dgf:tournament_attendance', get_test_tournament, get_id), 405),
        ('POST tournament attendance without existing one - logged in', LOGGED_IN, 'POST',
         ('dgf:tournament_attendance', get_test_tournament, get_id), 201),
        ('POST tournament attendance with existing one - logged in', LOGGED_IN, 'POST',
         ('dgf:tournament_attendance', get_test_tournament_with_attendance, get_id), 204),
        ('PUT tournament attendance PUT- logged in', LOGGED_IN, 'PUT',
         ('dgf:tournament_attendance', get_test_tournament, get_id), 405),
        ('PATCH tournament attendance - logged in', LOGGED_IN, 'PATCH',
         ('dgf:tournament_attendance', get_test_tournament, get_id), 405),
        ('DELETE tournament attendance without existing one - logged in', LOGGED_IN, 'DELETE',
         ('dgf:tournament_attendance', get_test_tournament, get_id), 204),
        ('DELETE tournament attendance with existing one - logged in', LOGGED_IN, 'DELETE',
         ('dgf:tournament_attendance', get_test_tournament_with_attendance, get_id), 204),

        ('GET bag tag claim - not logged in', NOT_LOGGED_IN, 'GET',
         ('dgf:bag_tag_claim', get_test_friend_with_bag_tag, get_bag_tag), (302, '/login')),

        ('GET bag tag claim - logged in', LOGGED_IN, 'GET',
         ('dgf:bag_tag_claim', get_test_friend_with_bag_tag, get_bag_tag), 405),
        ('POST bag tag claim - logged in', LOGGED_IN, 'POST',
         ('dgf:bag_tag_claim', get_test_friend_with_bag_tag, get_bag_tag), 204),
        ('PUT bag tag claim - logged in', LOGGED_IN, 'PUT',
         ('dgf:bag_tag_claim', get_test_friend_with_bag_tag, get_bag_tag), 405),
        ('PATCH bag tag claim - logged in', LOGGED_IN, 'PATCH',
         ('dgf:bag_tag_claim', get_test_friend_with_bag_tag, get_bag_tag), 405),
        ('DELETE bag tag claim - logged in', LOGGED_IN, 'DELETE',
         ('dgf:bag_tag_claim', get_test_friend_with_bag_tag, get_bag_tag), 405),

        ('GET bag tag new - not logged in', NOT_LOGGED_IN, 'GET', 'dgf:bag_tag_new', (302, '/login')),

        ('GET bag tag new - logged in', LOGGED_IN, 'GET', 'dgf:bag_tag_new', 405),
        ('POST bag tag new - logged in', LOGGED_IN, 'POST', 'dgf:bag_tag_new', 204),
        ('PUT bag tag new - logged in', LOGGED_IN, 'PUT', 'dgf:bag_tag_new', 405),
        ('PATCH bag tag new - logged in', LOGGED_IN, 'PATCH', 'dgf:bag_tag_new', 405),
        ('DELETE bag tag new - logged in', LOGGED_IN, 'DELETE', 'dgf:bag_tag_new', 405),

        ('GET bag tag update - not logged in', NOT_LOGGED_IN, 'GET', 'dgf:bag_tag_update', (302, '/login')),

        ('GET bag tag update - logged in', LOGGED_IN, 'GET', 'dgf:bag_tag_update', 405),
        ('POST bag tag update - logged in', LOGGED_IN, 'POST', 'dgf:bag_tag_update', 204),
        ('PUT bag tag update - logged in', LOGGED_IN, 'PUT', 'dgf:bag_tag_update', 405),
        ('PATCH bag tag update - logged in', LOGGED_IN, 'PATCH', 'dgf:bag_tag_update', 405),
        ('DELETE bag tag update - logged in', LOGGED_IN, 'DELETE', 'dgf:bag_tag_update', 405),
    ])
    @override_settings(ROOT_URLCONF='dgf.test.urls')
    def test_dgf_views(self, name, logged_in, method, url, expected):

        if logged_in:
            self.login()

        if type(url) == tuple:
            url_name, get_obj, get_field = url
            args = [get_field(get_obj())]
        else:
            url_name = url
            args = []

        response = self.client.generic(method, reverse(url_name, args=args))

        if type(expected) == tuple:
            expected_status_code, expected_url = expected
        else:
            expected_status_code = expected
            expected_url = None

        self.assertEqual(response.status_code, expected_status_code, msg=f'Unexpected status code for URL {url}')
        if expected_url:
            self.assertTrue(response.url.startswith(expected_url))
