from django.test import override_settings
from django.urls import reverse

from dgf.models import Friend
from dgf.test.integration.client_test import ClientTest


class BagTagsApi(ClientTest):

    def setUp(self):
        super().setUp()
        self.friend.bag_tag = 1
        self.friend.save()

    @override_settings(ROOT_URLCONF='dgf.test.urls')
    def test_bag_tag_update_anonymous_user(self):
        response = self.client.post(reverse('dgf:bag_tag_update'), data={})
        self.assertEqual(response.status_code, 302)

    @override_settings(ROOT_URLCONF='dgf.test.urls')
    def test_bag_tag_update_user_without_bag_tag(self):
        self.friend.bag_tag = None
        self.friend.save()
        self.login()
        response = self.client.post(reverse('dgf:bag_tag_update'), data={})
        self.assertEqual(response.status_code, 400)

    @override_settings(ROOT_URLCONF='dgf.test.urls')
    def test_bag_tag_update(self):
        self.login()

        # update all
        self.assert_that(having={'manolo': 2, 'fede': 3, 'jonas': 4},
                         setting={'manolo': 3, 'fede': 4, 'jonas': 2},
                         expect=204)

        # update but no change
        self.assert_that(having={'manolo': 2, 'fede': 3, 'jonas': 4},
                         setting={'manolo': 2, 'fede': 3, 'jonas': 4},
                         expect=204)

        # update but not all
        self.assert_that(having={'manolo': 2, 'fede': 3, 'jonas': 4},
                         setting={'manolo': 4, 'jonas': 2},
                         expect=204)

        # update but no changes
        self.assert_that(having={'manolo': 2, 'fede': 3, 'jonas': 4},
                         setting={'manolo': 2, 'fede': 3},
                         expect=204)

        # update one but no change
        self.assert_that(having={'manolo': 2, 'fede': 3, 'jonas': 4},
                         setting={'manolo': 2},
                         expect=204)

        # update nothing
        self.assert_that(having={'manolo': 2, 'fede': 3, 'jonas': 4},
                         setting={},
                         expect=204)

        # duplicated bag tag
        self.assert_that(having={'manolo': 2, 'fede': 3, 'jonas': 4},
                         setting={'manolo': 2, 'fede': 2, 'jonas': 3},
                         expect=400)

        # update one but not allowed
        self.assert_that(having={'manolo': 2, 'fede': 3, 'jonas': 4},
                         setting={'fede': 2},
                         expect=400)

        # update with wrong bag tags
        self.assert_that(having={'manolo': 2, 'fede': 3, 'jonas': 4},
                         setting={'fede': 2, 'manolo': 4},
                         expect=400)

        # update with unassigned bag tags
        self.assert_that(having={'manolo': 2, 'fede': 4, 'jonas': 5},
                         setting={'manolo': 2, 'fede': 3},
                         expect=204)

        # update with other unassigned bag tags
        self.assert_that(having={'manolo': 2, 'fede': 4, 'jonas': 5},
                         setting={'fede': 2, 'manolo': 3},
                         expect=204)

        # update with unassigned bag tags bigger than the worst given bag tag
        self.assert_that(having={'manolo': 2, 'fede': 4, 'jonas': 5},
                         setting={'fede': 2, 'manolo': 5},
                         expect=400)

        # update one to unassigned bag tag
        self.assert_that(having={'manolo': 3, 'fede': 4, 'jonas': 5},
                         setting={'manolo': 2},
                         expect=204)

        # update one to a bag tags bigger than the worst given bag tag
        self.assert_that(having={'manolo': 3, 'fede': 4, 'jonas': 5},
                         setting={'manolo': 6},
                         expect=400)

    def assert_that(self, having=None, setting=None, expect=204):
        having = having or {}
        setting = setting or {}

        Friend.objects.exclude(id=self.friend.id).delete()

        for username, bag_tag in having.items():
            Friend.objects.create(username=username, bag_tag=bag_tag)

        response = self.client.post(reverse('dgf:bag_tag_update'), data=setting)
        self.assertEqual(response.status_code, expect)

        if expect == 204:
            db_state = setting
        else:
            db_state = having

        for username, bag_tag in db_state.items():
            friend = Friend.objects.get(username=username)
            self.assertEqual(friend.bag_tag, bag_tag)
