import json
import uuid

from django.test import Client, TestCase
from django.test import override_settings
from django.urls import reverse

from dgf.models import Friend


class DiscGolfMetrixApi(TestCase):

    def setUp(self):
        self.client = Client()
        Friend.objects.all().delete()

    @override_settings(ROOT_URLCONF='dgf.test.urls')
    def test_all_friend_ids(self):

        self.assert_that(having_metrix_ids=[],
                         expect_metrix_ids={})

        self.assert_that(having_metrix_ids=[None],
                         expect_metrix_ids={})

        self.assert_that(having_metrix_ids=[None, None],
                         expect_metrix_ids={})

        self.assert_that(having_metrix_ids=[1],
                         expect_metrix_ids={1})

        self.assert_that(having_metrix_ids=[1, None],
                         expect_metrix_ids={1})

        self.assert_that(having_metrix_ids=[1, 2, 3],
                         expect_metrix_ids={1, 2, 3})

        self.assert_that(having_metrix_ids=[1, 2, None, 3],
                         expect_metrix_ids={1, 2, 3})

    def assert_that(self, having_metrix_ids=None, expect_metrix_ids=None):
        having_metrix_ids = having_metrix_ids or []
        expect_metrix_ids = expect_metrix_ids or {}

        for metrix_id in having_metrix_ids:
            Friend.objects.create(username=uuid.uuid4(), metrix_user_id=metrix_id)

        response = self.client.get(reverse('dgf:disc_golf_metrix_all_friend_ids'))
        self.assertEqual(response.status_code, 200)

        ids = set(json.loads(response.content)['ids'])
        expected_ids = {str(metrix_id) for metrix_id in expect_metrix_ids}
        self.assertEqual(ids, expected_ids)
